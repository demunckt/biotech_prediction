import json
import boto3
import pandas as pd
import io
import os

# --- CONFIGURATION ---
# PASTE YOUR EXACT ENDPOINT NAMES HERE
ENDPOINT_AFFINITY = 'ENDPOINT PLACEHOLDER'
ENDPOINT_ACTIVITY = 'ENDPOINT PLACEHOLDER'

s3_client = boto3.client('s3')
sm_runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    print("🧪 Biotech Screener started...")
    
    # 1. GET THE UPLOADED FILE DETAILS
    # The event comes from S3 PutObject trigger
    try:
        # Get the bucket name and file key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        print(f"📂 Processing file: s3://{bucket_name}/{file_key}")
    except (KeyError, IndexError):
        return {
            'statusCode': 400, 
            'body': json.dumps("Error: Event structure not recognized. Was this triggered by S3?")
        }

    # 2. READ THE FILE FROM S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read()
    except Exception as e:
        print(f"❌ Error reading file from S3: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Error reading file: {str(e)}")}
    
    # Determine file type (CSV or Parquet)
    try:
        if file_key.endswith('.parquet'):
            df = pd.read_parquet(io.BytesIO(file_content))
        else:
            df = pd.read_csv(io.BytesIO(file_content))
        print(f"📊 Loaded {len(df)} molecules.")
    except Exception as e:
        print(f"❌ Error parsing file: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Error parsing file: {str(e)}")}

    # 3. PREPARE PAYLOAD FOR ENDPOINTS
    # CRITICAL FIX: Drop the target columns (answers) and IDs before sending to the model
    # We create a temporary 'clean' dataframe just for prediction
    cols_to_drop = ['binding_affinity', 'active', 'compound_id', 'protein_id', 'Unnamed: 0']
    df_clean = df.drop(cols_to_drop, axis=1, errors='ignore')
    
    # Send only the features the model expects
    payload = df_clean.to_json(orient='records')

    # 4. INVOKE ACTIVITY MODEL (Classification)
    print(f"🚀 Invoking Activity Endpoint: {ENDPOINT_ACTIVITY}")
    try:
        response_act = sm_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_ACTIVITY,
            ContentType='application/json',
            Body=payload
        )
        result_act = json.loads(response_act['Body'].read().decode())
    except Exception as e:
        print(f"❌ Error invoking Activity Endpoint: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Activity Endpoint Error: {str(e)}")}
    
    # 5. INVOKE AFFINITY MODEL (Regression)
    print(f"🚀 Invoking Affinity Endpoint: {ENDPOINT_AFFINITY}")
    try:
        response_aff = sm_runtime.invoke_endpoint(
            EndpointName=ENDPOINT_AFFINITY,
            ContentType='application/json',
            Body=payload
        )
        result_aff = json.loads(response_aff['Body'].read().decode())
    except Exception as e:
        print(f"❌ Error invoking Affinity Endpoint: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Affinity Endpoint Error: {str(e)}")}

    # 6. COMBINE RESULTS
    # We add the predictions back to the original dataframe
    # Assuming the order is preserved (standard behavior)
    df['predicted_activity'] = result_act
    df['predicted_affinity'] = result_aff
    
    # Optional: Add a "Priority Score" logic
    # We mark it "High Priority" if Active=1 and Affinity > 6.0
    # Note: 'predicted_activity' might be [0, 1] or strings depending on model output
    # Ensure consistent types for comparison
    df['priority_candidate'] = df.apply(
        lambda x: 'YES' if (float(x['predicted_activity']) == 1.0 and float(x['predicted_affinity']) > 6.0) else 'NO', 
        axis=1
    )

    # 7. SAVE RESULTS TO S3
    # We save to a 'results/' folder to avoid triggering the Lambda again
    # Construct output key
    filename = os.path.basename(file_key)
    name_root, ext = os.path.splitext(filename)
    output_key = f"results/{name_root}_screened.csv"
        
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=csv_buffer.getvalue()
        )
        print(f"✅ Results saved to: s3://{bucket_name}/{output_key}")
    except Exception as e:
        print(f"❌ Error saving results to S3: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Error saving results: {str(e)}")}
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Screening complete. Results at {output_key}")
    }
    
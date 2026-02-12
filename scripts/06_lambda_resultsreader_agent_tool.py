import json
import boto3
import pandas as pd
import io

s3_client = boto3.client('s3')
BUCKET_NAME = 'BUCKET PLACEHOLDER'

def lambda_handler(event, context):
    # --- 1. FIND AND READ DATA (Same as before) ---
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix='results/')
        files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
        latest_file = files[0]['Key']
        
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=latest_file)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        
        hits = df[df['priority_candidate'] == 'YES']
        num_hits = len(hits)
        top_hits = hits.sort_values(by='predicted_affinity', ascending=False).head(3)
        
        details = [f"Mol {r['compound_id']}: Aff {round(r['predicted_affinity'],2)}" for _, r in top_hits.iterrows()]
        summary = f"Found {num_hits} hits in {latest_file}. Top leads: {', '.join(details)}"
        
    except Exception as e:
        summary = f"Error processing results: {str(e)}"

    # --- 2. THE CRITICAL BEDROCK RESPONSE FORMAT ---
    # Bedrock needs to see 'actionGroup', 'function', and 'functionResponse'
    action_group = event.get('actionGroup')
    function = event.get('function')
    
    response_body = {
        'TEXT': {
            'body': summary
        }
    }

    function_response = {
        'actionGroup': action_group,
        'function': function,
        'functionResponse': {
            'responseBody': response_body
        }
    }

    session_attributes = event.get('sessionAttributes', {})
    prompt_session_attributes = event.get('promptSessionAttributes', {})

    return {
        'response': function_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
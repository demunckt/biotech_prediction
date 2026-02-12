import pandas as pd
import boto3
import os
from sklearn.preprocessing import StandardScaler

# =================CONFIGURATION=================
# 🔑 AWS CONFIG
# (We use os.getenv to be safe, or you can hardcode for this run)
AWS_ACCESS_KEY = 'PLACEHOLDER KEY'
AWS_SECRET_KEY = 'PLACEHOLDER KEY'
REGION = 'REGION PLACEHOLDER'

BUCKET_NAME = 'BUCKET NAME'
LOCAL_INPUT = 'INPUT PATH'
LOCAL_OUTPUT = 'PARQUET'
S3_OUTPUT_KEY = 'OUTPUT KEY'
# ===============================================

def engineer_features():
    # 1. Load Data
    if not os.path.exists(LOCAL_INPUT):
        print(f"❌ Error: {LOCAL_INPUT} not found. Make sure you are in the project folder!")
        return

    print(f"📖 Reading {LOCAL_INPUT}...")
    df = pd.read_csv(LOCAL_INPUT)

    # 2. Define Columns to Scale
    # We remove IDs and Targets so we only scale the chemistry numbers
    exclude_cols = ['compound_id', 'protein_id', 'active', 'binding_affinity']
    feature_cols = [c for c in df.columns if c not in exclude_cols]

    print(f"⚖️  Standardizing {len(feature_cols)} features (Mean=0, Std=1)...")

    # 3. Apply Standard Scaling
    # This is CRITICAL for the Linear Regression model to work correctly
    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    # 4. Save to Parquet (The standard format for AI)
    df.to_parquet(LOCAL_OUTPUT, index=False)
    print(f"✅ Saved local Gold file: {LOCAL_OUTPUT}")

    # 5. Upload to S3
    print(f"🚀 Uploading to s3://{BUCKET_NAME}/{S3_OUTPUT_KEY}...")
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION)
    
    s3.upload_file(LOCAL_OUTPUT, BUCKET_NAME, S3_OUTPUT_KEY)
    print("🎉 Success! Gold Data is ready for SageMaker.")

if __name__ == "__main__":
    engineer_features()
import boto3
import os

# =================CONFIGURATION=================
# 🔑 PASTE YOUR KEYS HERE (Keep them safe!)
AWS_ACCESS_KEY = 'PLACEHOLDER KEY'
AWS_SECRET_KEY = 'PLACEHOLDER KEY'
REGION = 'eu-north-1' # Standard region

# 📦 NAME YOUR BUCKET (Must be globally unique)
BUCKET_NAME = 'BUCKET NAME PLACEHOLDER'

# Files to upload (Local Path -> S3 Path)
FILES = {
    'folder_placeholder': 'bronze/train_dataset.csv',
    'folder': 'bronze/blind_test.csv'
}
# ===============================================

def upload_to_s3():
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION)

    # 1. Create Bucket
    try:
        if REGION == 'us-east-1':
            s3.create_bucket(Bucket=BUCKET_NAME)
        else:
            s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': REGION})
        print(f"✅ Bucket '{BUCKET_NAME}' ready.")
    except Exception as e:
        if "BucketAlreadyOwnedByYou" in str(e):
            print(f"✅ Bucket '{BUCKET_NAME}' found.")
        else:
            print(f"❌ Error: {e}"); return

    # 2. Upload
    for local, remote in FILES.items():
        if os.path.exists(local):
            print(f"🚀 Uploading {local} -> s3://{BUCKET_NAME}/{remote}")
            s3.upload_file(local, BUCKET_NAME, remote)
        else:
            print(f"⚠️ File missing: {local} (Did you run the split cell?)")

if __name__ == "__main__":
    upload_to_s3()
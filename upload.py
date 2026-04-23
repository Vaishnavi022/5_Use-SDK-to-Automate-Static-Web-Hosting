import boto3
import os
import json
import mimetypes
import botocore

# =========================
# CONFIG
# =========================
bucket_name = "my-static-site-disha-12345"
region = "ap-south-1"

s3 = boto3.client('s3')

# =========================
# STEP 1: CREATE BUCKET
# =========================
print("Creating bucket...")

try:
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region}
    )
    print("Bucket created successfully!")

except botocore.exceptions.ClientError as e:
    error_code = e.response['Error']['Code']

    if error_code == 'BucketAlreadyOwnedByYou':
        print("Bucket already exists. Continuing...")
    else:
        raise

# =========================
# STEP 2: UPLOAD FILES
# =========================
print("Uploading files...")

for file in os.listdir():
    if os.path.isfile(file):
        content_type, _ = mimetypes.guess_type(file)

        extra_args = {}

        if content_type:
            extra_args['ContentType'] = content_type

        # ❌ REMOVED ACL (IMPORTANT FIX)

        s3.upload_file(
            file,
            bucket_name,
            file,
            ExtraArgs=extra_args
        )

print("Files uploaded successfully!")

# =========================
# STEP 3: APPLY BUCKET POLICY
# =========================
print("Applying bucket policy...")

bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }
    ]
}

try:
    s3.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(bucket_policy)
    )
    print("Bucket policy applied!")

except botocore.exceptions.ClientError as e:
    print("Policy error:", e)

# =========================
# STEP 4: ENABLE STATIC HOSTING
# =========================
print("Enabling static website hosting...")

s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'index.html'},
        'ErrorDocument': {'Key': 'error.html'}
    }
)

# =========================
# FINAL OUTPUT
# =========================
print("\n🚀 Deployment complete!")

print("\n🌐 Website URL:")
print(f"http://my-static-site-disha-12345.s3-website.ap-south-1.amazonaws.com/")
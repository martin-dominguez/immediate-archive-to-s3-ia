import boto3

# Function that gets elements from a s3 bucket filtered by the standard storage class
def move_objects_to_ia(bucket_name, account_id, prefix=''):
    # Create an S3 client
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')

    # List objects in the bucket with the specified storage class
    try:
        pages = paginator.paginate(
            Bucket=bucket_name,
            Prefix=prefix
        )
    except Exception as e:
        print(f"Error listing objects: {e}")
        return
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['StorageClass'] == 'STANDARD':
                    object_key = obj['Key']
                    copy_source = {
                        'Bucket': bucket_name,
                        'Key': object_key
                    }
                    try:
                        s3.copy_object(
                            Bucket=bucket_name,
                            Key=object_key,
                            CopySource=copy_source,
                            StorageClass='STANDARD_IA',
                            ExpectedBucketOwner=account_id,
                            ExpectedSourceBucketOwner=account_id
                        )
                        print(f"Moved object {object_key} to STANDARD_IA storage class.")
                    except Exception as e:
                        print(f"Error moving object {object_key}: {e}")

# Main lambda handler
def lambda_handler(event, context):
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']

    move_objects_to_ia(
        bucket_name=event['bucket_name'],
        account_id=account_id,
        prefix=event.get('prefix', '')
    )
    return {
        'statusCode': 200,
        'body': 'Objects moved to STANDARD_IA storage class successfully.'
    }

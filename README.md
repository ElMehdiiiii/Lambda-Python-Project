# Lambda Project: Organizing S3 Storage by Date Directory

This AWS Lambda function is designed to organize the files in an S3 bucket into directories based on their last modified date. The function runs daily, moving each file into a directory named with the current date in `YYYYMMDD` format.

## Prerequisites

- AWS account
- S3 bucket named `elafkaihi-artifacts`
- IAM role with permissions to execute Lambda functions and access S3 operations

## Project Structure

- `lambda_function.py`: Contains the code for the Lambda function.

## Code Explanation

The Lambda function performs the following steps:

1. **Import Libraries**: Import the `boto3` library to interact with AWS services and `datetime` to handle date operations.
2. **Get Today's Date**: Retrieve the current date in `YYYYMMDD` format.
3. **Initialize S3 Client**: Create an S3 client using `boto3`.
4. **List Objects in the Bucket**: List all objects in the specified S3 bucket.
5. **Create Date Directory**: Check if a directory for today's date exists; if not, create it.
6. **Move Files**: For each file, check its last modified date. If it matches today's date and is not already in a directory, move it to the appropriate date directory.

## Lambda Function Code

```python
import boto3
from datetime import datetime

today = datetime.today()
today_date = today.strftime("%Y%m%d")

def lambda_handler(event, context):
    client = boto3.client('s3')

    bucket_name = "elafkaihi-artifacts"
    response = client.list_objects_v2(Bucket=bucket_name)

    get_content = response['Contents']

    get_all_files_name = []
    for file in get_content:
        get_all_files_name.append(file['Key'])

    directory_name = today_date + "/"

    if directory_name not in get_all_files_name:
        client.put_object(Bucket=bucket_name, Key=directory_name)

    for item in get_content:
        object_date = item.get("LastModified").strftime("%Y%m%d") + "/"
        object_name = item.get("Key")
        if object_date == directory_name and "/" not in object_name:
            client.copy_object(CopySource=bucket_name + "/" + object_name, Bucket=bucket_name, Key=directory_name + object_name)
            client.delete_object(Bucket=bucket_name, Key=object_name)
```

## Deployment Instructions

1. **Create the Lambda Function**:
   - Go to the AWS Lambda console.
   - Click on "Create function".
   - Choose "Author from scratch".
   - Provide a function name and select the appropriate runtime (e.g., Python 3.8).
   - Click "Create function".

2. **Set Up Permissions**:
   - Attach a policy to the Lambda execution role that allows read and write access to the S3 bucket `elafkaihi-artifacts`.

3. **Add the Code**:
   - In the Lambda function console, replace the default code with the provided `lambda_function.py` code.
   - Click "Deploy" to save the changes.

4. **Test the Function**:
   - Create a test event with any dummy data (the function does not rely on event data).
   - Run the test to ensure the function executes without errors.

5. **Set Up a Trigger**:
   - Add a S3:Put to trigger the Lambda function daily.

## Notes
- Modify the bucket name in the code if you are using a different bucket.


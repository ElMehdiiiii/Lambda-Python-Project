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
    for file in get_content : 
        get_all_files_name.append(file['Key'])

    directory_name = today_date + "/"

    if directory_name not in get_all_files_name:
        client.put_object(Bucket=bucket_name, Key=directory_name)

    for item in get_content:
        object_date = item.get("LastModified").strftime("%Y%m%d") +"/"
        object_name = item.get("Key")
        if object_date == directory_name and "/" not in object_name:
            client.copy_object(CopySource=bucket_name+"/"+object_name, Bucket=bucket_name, Key=directory_name+object_name)
            client.delete_object(Bucket=bucket_name, Key=object_name)



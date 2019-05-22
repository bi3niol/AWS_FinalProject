import uuid
import boto3
import json
from pathlib import Path
import base64

BUCKET_NAME = "chmury.website.images"
IMAGE_FOLDER_PATH = Path("images")
LOCAL_TMP_PATH = Path("/tmp")

def save_to_local_file(filename, base64data):
    barray = bytearray(base64data)
    filePath = LOCAL_TMP_PATH / filename
    with open(filePath,"wb") as file:
        fh.write(base64.decodebytes(barray))

    return filePath

s3 = boto3.resource('s3')

def lambda_handler(event,context):
    model = event["body"]
    filename = model["filename"]
    imagedata = model["imagedata"]
    contenttype = model["contenttype"]
    
    file_destination = IMAGE_FOLDER_PATH / filename

    localFile = save_to_local_file(filename,imagedata)

    unique_filename = f"{str(uuid.uuid4())}_{filename}"

    bucketFilePath = IMAGE_FOLDER_PATH / unique_filename

    s3.meta.client.upload_file(str(localFile),BUCKET_NAME, str(bucketFilePath))

    return {
        'body' : str(bucketFilePath)
        }
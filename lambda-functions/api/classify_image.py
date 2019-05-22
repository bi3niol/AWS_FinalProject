import uuid
import boto3
import json
from pathlib import Path
import base64

BUCKET_NAME = "chmury.website.images"
IMAGE_FOLDER_PATH = Path("images")
LOCAL_TMP_PATH = Path("/tmp")

def save_to_local_file(filename, base64data):
    barray = bytearray(base64data, 'utf_8')
    filePath = LOCAL_TMP_PATH / filename
    with open(filePath,"wb") as file:
        file.write(base64.decodebytes(barray))

    return filePath

s3 = boto3.resource('s3')

reko = boto3.client('rekognition')

def lambda_handler(event,context):
    model = json.loads(event["body"])
    #model = event["body"]
    filename = model["filename"]
    imagedata = model["imagedata"]
    contenttype = model["contenttype"]
    
    file_destination = IMAGE_FOLDER_PATH / filename

    localFile: Path = save_to_local_file(filename,imagedata)

    unique_filename = f"{str(uuid.uuid4())}_{filename}"

    bucketFilePath = IMAGE_FOLDER_PATH / unique_filename

    s3.meta.client.upload_file(str(localFile),BUCKET_NAME, str(bucketFilePath))
    
    response = reko.detect_labels(
        Image={
            'S3Object': {
                'Bucket': BUCKET_NAME,
                'Name': str(bucketFilePath)
            }
        },
        MaxLabels=123
    )
    #print(response)
    
    
    return {
        'body' : "My Job done"
        }

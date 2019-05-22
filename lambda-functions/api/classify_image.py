import boto3
import json
from pathlib import Path
BUCKET_NAME = "chmury.website.images"
IMAGE_FOLDER_PATH = Path("images")

def save_to_local_file(filename, base64data):
    
    pass

def classify_image():
    return "cat", 80

s3 = boto3.client('s3')

def lambda_handler(event,context):
    model = json.loads(event["body"])
    filename = model["filename"]
    imagedata = model["imagedata"]
    contenttype = model["contenttype"]
    
    file_destination = IMAGE_FOLDER_PATH_FORMAT / filename

    pass
print(IMAGE_FOLDER_PATH_FORMAT / "hello.jpg")
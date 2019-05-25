import boto3
from datetime import datetime

CLASSIFIED_IMAGES_TABLE_NAME = "ClassifiedImages"
STATISTICS_DATA_TABLE_NAME = "StatisticsData"
CI_PRIMARY_KEY = "primarykey"

dynamodb = boto3.resource('dynamodb')


def get_top_n_classes(tablename: str, n: int = 10):
    pass


def add_classified_image(s3Location: str, s3Bucket, labels):
    table = dynamodb.Table(CLASSIFIED_IMAGES_TABLE_NAME)
    table.put_item(
        Item={
            CI_PRIMARY_KEY: s3Location,
            'labels': labels,
            'createdOn': str(datetime.now()),
            'bucketName': s3Bucket
        }
    )

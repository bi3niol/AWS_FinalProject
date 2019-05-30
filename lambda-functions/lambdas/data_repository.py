import boto3
import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
import copy

CLASSIFIED_IMAGES_TABLE_NAME = "ClassifiedImages"
STATISTICS_DATA_TABLE_NAME = "StatisticsData"

CI_PRIMARY_KEY = "primarykey"
CI_CREATEDON_KEY = "createdOn"
CI_BUCKET_NAME_NAME = "bucketName"
CI_LABELS_KEY = "labels"

STATISTICS_DATA_PRIMARY_KEY = "set_name"
STATISTICS_DATA_PRIMARY_KEY_VALUE = "aggregated_labels"
STATISTICS_DATA_LABELS_KEY = "labels"
STATISTICS_DATA_LAST_SYNC_KEY = "last_sync"

dynamodb = boto3.resource('dynamodb')


def get_statistics_data(projectionExpresion: str = None):
    table = dynamodb.Table(STATISTICS_DATA_TABLE_NAME)

    key = {
        STATISTICS_DATA_PRIMARY_KEY: STATISTICS_DATA_PRIMARY_KEY_VALUE
    }
    if projectionExpresion is None:
        response = table.get_item(Key=key)
    else:
        response = table.get_item(
            Key=key, ProjectionExpression=projectionExpresion)

    return response.get("Item", {})


def get_current_labels_state_of_statistics():
    sd = get_statistics_data()
    table = dynamodb.Table(CLASSIFIED_IMAGES_TABLE_NAME)

    response = table.scan(FilterExpression=Attr(
        CI_CREATEDON_KEY).gte(sd.get(STATISTICS_DATA_LAST_SYNC_KEY, str(datetime.date.min))))

    items = response.get("Items", [])

    labels = count_labels(items)

    sdLabels = sd.get(STATISTICS_DATA_LABELS_KEY, {})

    __merge_statistics(sdLabels, labels)

    labelArray = []
    for key in sdLabels:
        labelArray.append({"label": key, "count": labels[key]})

    labelArray.sort(key=lambda x: x['count'], reverse=True)

    return labelArray, sdLabels


def count_labels(classifiedImages):
    res = {}
    for ci in classifiedImages:
        for _class in ci.get("labels", []):
            if(not "Name" in _class):
                continue
            res[_class['Name']] = res.get(_class['Name'], 0) + 1
    return res


def __merge_statistics(statObject, labels):
    for key in labels:
        statObject[key] = statObject.get(key, 0) + labels[key]


def get_top_n_labels(n: int = 10):
    labels, _ = get_current_labels_state_of_statistics()
    nn = min(n, len(labels))
    return labels[0:nn]


def get_top_n_images(n: int = 20):
    projectionExpression = f"{CI_PRIMARY_KEY}, {CI_BUCKET_NAME_NAME}, {CI_CREATEDON_KEY}, {CI_LABELS_KEY}"
    # expressionAttributeNames = {
    #     "#location": CI_PRIMARY_KEY
    # }
    table = dynamodb.Table(CLASSIFIED_IMAGES_TABLE_NAME)
    response = table.scan(ProjectionExpression=projectionExpression,
                          # ExpressionAttributeNames=expressionAttributeNames,
                          Limit=n)

    return response.get("Items", [])


def add_classified_image(s3Location: str, s3Bucket, labels):
    table = dynamodb.Table(CLASSIFIED_IMAGES_TABLE_NAME)
    labels = copy.deepcopy(labels)

    for label in labels:
        label["Confidence"] = str(label["Confidence"])
        label.pop("Instances", None)
        label.pop("Parents", None)

    table.put_item(Item={
        CI_PRIMARY_KEY: s3Location,
        CI_LABELS_KEY: labels,
        CI_CREATEDON_KEY: str(datetime.datetime.now()),
        CI_BUCKET_NAME_NAME: s3Bucket
    })

    return labels

import boto3
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

CLASSIFIED_IMAGES_TABLE_NAME = "ClassifiedImages"
STATISTICS_DATA_TABLE_NAME = "StatisticsData"
CI_PRIMARY_KEY = "primarykey"
CI_CREATEDON_KEY = "createdOn"

STATISTICS_DATA_PRIMARY_KEY = "set_name"
STATISTICS_DATA_PRIMARY_KEY_VALUE = "aggregated_labels"
STATISTICS_DATA_LABELS_KEY = "labels"
STATISTICS_DATA_LAST_SYNC_KEY = "last_sync"

dynamodb = boto3.resource('dynamodb')


def get_statistics_data(projectionExpresion: str = None):
    table = dynamodb.Table(STATISTICS_DATA_TABLE_NAME)

    queryItem = {
        "Key": {
            STATISTICS_DATA_PRIMARY_KEY: STATISTICS_DATA_PRIMARY_KEY_VALUE
        }
    }

    if(projectionExpresion != None):
        queryItem["ProjectionExpression"] = projectionExpresion

    response = table.get_item(queryItem)

    if("Item" in response):
        return response["Item"]

    return None


def get_current_labels_state_of_statistics():
    sd = get_statistics_data()
    table = dynamodb.Table(CLASSIFIED_IMAGES_TABLE_NAME)

    items = None
    response = {}
    if(sd == None):
        response = table.scan()
    else:
        response = table.scan(FilterExpression=Attr(
            CI_CREATEDON_KEY).gte(sd[STATISTICS_DATA_LAST_SYNC_KEY]))

    if("Items" in response):
        items = response["Items"]
    else:
        items = []

    labels = count_labels(items)
    sdLabels = {}
    if(sd != None and STATISTICS_DATA_LABELS_KEY in sd):
        sdLabels = sd[STATISTICS_DATA_LABELS_KEY]

    __merge_statistics(sdLabels, labels)

    labelArray = []
    for key in sdLabels:
        labelArray.append({"label": key, "count": labels[key]})

    labelArray.sort(key=lambda x: x.count, reverse=True)

    return labelArray, sdLabels


def count_labels(classifiedImages):
    res = {}
    for ci in classifiedImages:
        for _class in ci["labels"]:
            if(not _class.Name in res):
                res[_class.Name] = 0
            res[_class.Name] = res[_class.Name] + 1
    return res


def __merge_statistics(statObject, labels):
    for key in labels:
        if(key in statObject):
            statObject[key] = statObject[key] + labels[key]
        else:
            statObject[key] = labels[key]


def get_top_n_labels(n: int = 10):
    labels, _ = get_current_labels_state_of_statistics()
    nn = min(n, len(labels))
    return labels[0:nn]


def add_classified_image(s3Location: str, s3Bucket, labels):
    table = dynamodb.Table(CLASSIFIED_IMAGES_TABLE_NAME)
    for label in labels:
        label["Confidence"] = str(label["Confidence"])

    table.put_item(Item={
        CI_PRIMARY_KEY: s3Location,
        'labels': labels,
        'createdOn': str(datetime.now()),
        'bucketName': s3Bucket
    })

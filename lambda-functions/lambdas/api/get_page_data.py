import data_repository as dal
import json


def lambda_handler(event, context):
    # TODO implement
    urlParams = None
    if("queryStringParameters" in event):
        urlParams = event["queryStringParameters"]
    labelCount = 10
    imageCount = 10
    if(urlParams != None):
        if("topLabelsCount" in urlParams):
            labelCount = int(urlParams["topLabelsCount"])
        if("imageCount" in urlParams):
            imageCount = int(urlParams["imageCount"])

    labels = dal.get_top_n_labels(labelCount)
    return {
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST"
        },
        'body': json.dumps({
            "labels": labels
        })
    }

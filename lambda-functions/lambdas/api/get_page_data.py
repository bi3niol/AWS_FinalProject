import data_repository as dal
import json


def lambda_handler(event, context):
    try:
        urlParams = event.get("queryStringParameters", {})

        labelCount = int(urlParams.get("topLabelsCount", 10))
        imageCount = int(urlParams.get("imageCount", 20))
        labels = dal.get_top_n_labels(labelCount)
        images = dal.get_top_n_images(imageCount)
        return {
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST"
            },
            'body': json.dumps({
                "labels": labels,
                "images": images
            })
        }
    except Exception as e:
        return {
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST"
            },
            'statusCode': 400,
            'body': str(e)
        }

import data_repository as dal
import os
import boto3

TOPIC_ARN = os.environ["TOPIC_ARN"]  # "chmury.website.images"

sns = boto3.client('sns')


def lambda_handler(event, context):
    dailyData = dal.update_statistics_and_get_daily_data()

    message = ["Daily Raport:"] + [f"{elem['label']}: {elem['count']}" for elem in dailyData]
    
    msg = "\n".join(message)

    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=msg,
    )

    print(response)

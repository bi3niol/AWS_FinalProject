import data_repository as dal


def lambda_handler(event, context):
    dailyData = dal.update_statistics_and_get_daily_data()
    # todo prepere daily raport, triger SNS event

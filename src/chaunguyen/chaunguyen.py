import logging
import traceback
import boto3
from src.chaunguyen.utils.music_crawler import crawl_music_chart_to_df
from src.chaunguyen.utils import variables as V
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    try:
        logger.info(f"EVENT: {event}")
        logger.info(f"CONTEXT: {context}")

        df = crawl_music_chart_to_df()
        music_data_csv = df.to_csv(index=False)

        # Initialize the S3 client
        s3_client = boto3.client('s3')

        # S3 bucket name, file name, object key
        bucket_name = V.DATA_LANDING_BUCKET_NAME
        file_name = f'music_chart_{(datetime.today() - timedelta(days=2)).strftime("%Y%m%d")}.csv'
        object_key = f'chaunguyen/raw/{file_name}'

        # Upload the csv to S3
        s3_client.put_object(Bucket=bucket_name, 
                             Key=object_key, 
                             Body=music_data_csv)

        logger.info(f'Successfully uploaded the csv to s3://{bucket_name}/{object_key}')
        return {"status": "SUCCESS"}
    except Exception as ex:
        logger.error(f'FATAL ERROR: {ex} %s')
        logger.error('TRACEBACK:')
        logger.error(traceback.format_exc())

        return {"status": "FAIL", "error": f"{ex}"}

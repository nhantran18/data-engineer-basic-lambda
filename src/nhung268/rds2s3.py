import logging
import traceback
import boto3

from src.common.db_utils import create_connection, fetch_data_by_sql, create_binary_from_list_data
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    try:
        logger.info(f"EVENT: {event}")
        logger.info(f"CONTEXT: {context}")

        # Add table name to get data in specific table in RDS
        # included schema.table_name
        # Eg: ai4e_test.account
        table_name = event['table_name'] # -> SQL cu the
        
        # S3 info that stores physical data when we ingest into datalake
        bucket_name = event['bucket_name']
        object_key: str = event['object_key']

        # Crawl data from source --- START
        connection = create_connection()

        query_str_sql = f"select * from {table_name}"
        results = fetch_data_by_sql(connection, query_str_sql)

        csv_binary = create_binary_from_list_data(results)
        # Crawl data from source --- END

        # SAVE DATA into S3 storage -- START
        client = boto3.client('s3')
        client.put_object(
            Body=csv_binary.read(), 
            Bucket=bucket_name,
            Key=object_key[1:] if object_key.startswith('/') else object_key
        )
        # SAVE DATA into S3 storage -- END
        connection.close()
        return {"status": "SUCCESS"}
    except Exception as ex:
        logger.error(f'FATAL ERROR: {ex} %s')
        logger.error('TRACEBACK:')
        logger.error(traceback.format_exc())
        return {"status": "FAIL", "error": f"{ex}"}

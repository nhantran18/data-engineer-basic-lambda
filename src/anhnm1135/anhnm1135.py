import logging
import traceback
import boto3
import json
from datetime import datetime
from src.anhnm1135.utils.crawler import crawler_cafef

from src.common.db_utils import create_connection, fetch_data_by_sql, create_binary_from_list_data
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


s3_client = boto3.client('s3')

def lambda_handler(event, context):

    df = crawler_cafef()
    csv_data = df.to_csv(index=False)

    #datetime 
    # current_time = datetime.now()
    # date_string = f"{str(current_time.year)}-{str(current_time.month).zfill(2)}-{str(current_time.day).zfill(2)}"
    # csv_data = csv_data[csv_data['cob_dt'] == date_string]

    # Thông tin về S3 bucket và tên file
    bucket_name = 'ai4e-ap-southeast-1-dev-s3-data-landing'
    file_name = f"anhnm1135/data/cafef_{datetime.now().strftime('%Y-%m-%d')}.csv"

    try:
        # Đẩy dữ liệu CSV lên S3 trực tiếp từ bộ nhớ
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=csv_data
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Dữ liệu đã được đẩy lên S3 thành công!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Có lỗi xảy ra: {str(e)}')
        }
    
# def lambda_handler(event, context):
#     try:
#         logger.info(f"EVENT: {event}")
#         logger.info(f"CONTEXT: {context}")

#         # Add table name to get data in specific table in RDS
#         # included schema.table_name
#         # Eg: ai4e_test.account
#         # table_name = event['table_name'] # -> SQL cu the
        
#         # S3 info that stores physical data when we ingest into datalake
#         bucket_name = 'ai4e-ap-southeast-1-dev-s3-data-landing/anhnm1135'
#         # object_key: str = event['object_key']

#         # # Crawl data from source --- START
#         # connection = create_connection()

#         # query_str_sql = f"select * from {table_name}"
#         # results = fetch_data_by_sql(connection, query_str_sql)

#         # csv_binary = create_binary_from_list_data(results)
#         # # Crawl data from source --- END

#         # # SAVE DATA into S3 storage -- START
#         # client = boto3.client('s3')
#         # client.put_object(
#         #     Body=csv_binary.read(), 
#         #     Bucket=bucket_name,
#         #     Key=object_key[1:] if object_key.startswith('/') else object_key
#         # )
#         # # SAVE DATA into S3 storage -- END
#         # connection.close()
#         return {"status": "SUCCESS"}
#     except Exception as ex:
#         logger.error(f'FATAL ERROR: {ex} %s')
#         logger.error('TRACEBACK:')
#         logger.error(traceback.format_exc())
#         return {"status": "FAIL", "error": f"{ex}"}

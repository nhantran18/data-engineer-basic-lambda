import boto3
import os
import traceback
import logging
from src.lmq0411.utils.main import crawl  

# Cấu hình logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"EVENT: {event}")
        logger.info(f"CONTEXT: {context}")

        output_file = '/tmp/real_estate_data.csv'  
        
        # Gọi hàm crawl từ main.py
        base_url = 'https://batdongsan.com.vn/nha-dat-ban'
        property_type = 'Nhà'
        max_pages = 9000
        
        crawl(base_url, property_type, output_file=output_file, max_pages=max_pages)

        # Khởi tạo S3 client
        s3_client = boto3.client('s3')
        
        # Specify S3 Bucket and Object
        bucket_name = os.environ['DATA_LANDING_BUCKET_NAME']  
        s3_saving_path = f'bronze/{os.path.basename(output_file)}'  
        
        # Upload file CSV vào S3
        with open(output_file, 'rb') as data:
            s3_client.put_object(
                Body=data, 
                Bucket=bucket_name,
                Key=s3_saving_path  
            )

        logger.info(f'Successfully uploaded the file to s3://{bucket_name}/{s3_saving_path}')

        return {"status": "SUCCESS"}
    
    except Exception as ex:
        logger.error(f'FATAL ERROR: {ex}')
        logger.error('TRACEBACK:')
        logger.error(traceback.format_exc())

        return {"status": "FAIL", "error": f"{ex}"}

import time
import csv
from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from .utils.movie_crawler_utils import crawl_box_office, create_csv_data
import logging
import traceback
import boto3
from src.common.db_utils import create_connection, fetch_data_by_sql, create_binary_from_list_data


# Create a timezone for UTC-7
utc_minus_7 = timezone(timedelta(hours=-7))

# Get the current datetime in UTC-7
utc_datetime = datetime.now(utc_minus_7)

# Subtract one day to get the previous day
prev_day_datetime = utc_datetime - timedelta(days=1)
utc_iso_str = prev_day_datetime.strftime("%Y-%m-%d")

#Url of website need to be crawled
pre_url = "https://www.boxofficemojo.com/date"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    try:
        logger.info(f"EVENT: {event}")
        logger.info(f"CONTEXT: {context}")

        bucket_name = "ai4e-ap-southeast-1-dev-s3-data-landing" 
        # object_key = f"nhantran/data/{utc_iso_str}.csv"
        object_key = f"nhantran/data/{event['data_date']}.csv"

        # movie_lists = crawl_box_office(pre_url, utc_iso_str)
        movie_lists = crawl_box_office(pre_url, event['data_date'])


        csv_binary = create_csv_data(movie_lists)

        client = boto3.client('s3')
        client.put_object(
            Body=csv_binary,
            Bucket=bucket_name,
            Key=object_key
        )

        return {"status": "SUCCESS"}
    except Exception as ex:
        logger.error(f'FATAL ERROR: {ex} %s')
        logger.error('TRACEBACK:')
        logger.error(traceback.format_exc())
        return {"status": "FAIL", "error": f"{ex}"}
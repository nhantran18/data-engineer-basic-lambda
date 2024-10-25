import os
import sys


# Getting to the Lambda directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
from src.nhantran.movie_crawl import lambda_handler
# from tests.common.utils import get_event_input_by_path


def test():
    path_input = "ai4e_crawler/event_imdb.json"
    event = {
        "url": "https://www.boxofficemojo.com/date/",
        "schema_name": "hanhtd2_imdb",
        "table_name": "ai4e_movie",
        "data_field": [
            {
                "field": "rank_in_today",
                "type": "varchar"
            },
            {
                "field": "rank_in_yesterday",
                "type": "varchar"
            },
            {
                "field": "movie_name",
                "type": "varchar"
            },
            {
                "field": "movie_link",
                "type": "varchar"
            },
            {
                "field": "movie_release_id",
                "type": "varchar"
            },
            {
                "field": "movie_title_id",
                "type": "varchar"
            },
            {
                "field": "daily_gross",
                "type": "varchar"
            },
            {
                "field": "day_gross_change",
                "type": "varchar"
            },
            {
                "field": "week_gross_change",
                "type": "varchar"
            },
            {
                "field": "number_of_theater",
                "type": "varchar"
            },
            {
                "field": "avg_per_theater",
                "type": "varchar"
            },
            {
                "field": "gross_to_date",
                "type": "varchar"
            },
            {
                "field": "num_of_day_release",
                "type": "varchar"
            },
            {
                "field": "distributor",
                "type": "varchar"
            },
            {
                "field": "date_crawled",
                "type": "varchar"
            }
        ],
    }
    context = None
    
    from datetime import date, timedelta

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    start_date = date(2024, 9, 1)
    end_date = date(2024, 10, 6)
    for single_date in daterange(start_date, end_date):
        print(single_date.strftime("%Y-%m-%d"))
        event['data_date'] = single_date.strftime("%Y-%m-%d")
        payload = lambda_handler(event, context)
        print(payload)
    assert 1 == 1


if __name__ == '__main__':
    test()

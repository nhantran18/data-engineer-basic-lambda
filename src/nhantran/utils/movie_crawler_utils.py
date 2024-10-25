import time
import csv
import io
from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import dataclass

@dataclass
class Movie:
    rank_today: str
    rank_yesterday: str
    name: str
    today_revenue: str
    gross_change_per_day: str
    gross_change_per_week: str
    num_of_theaters: str
    avg_revenue_per_theater: str
    total_revenue: str
    total_day: str
    distributor: str

    def __str__(self):
        return f"""{self.rank_today}, {self.rank_yesterday}, {self.name}, {self.today_revenue}, {self.gross_change_per_day}, {self.gross_change_per_week}, {self.num_of_theaters}, {self.avg_revenue_per_theater}, {self.total_revenue}, {self.total_day}, {self.distributor}"""

    def writeToCSV(self):
        return [self.rank_today, self.rank_yesterday, self.name, self.today_revenue, self.gross_change_per_day, self.gross_change_per_week, self.num_of_theaters, self.avg_revenue_per_theater, self.total_revenue, self.total_day, self.distributor]

def crawl_box_office(url: str, date='2000-01-01'):
    # Initialize the Chrome browser
    driver = webdriver.Chrome()
    driver.get(f"{url}/{date}/")

    movie_lists = []
    i = 0

    while True:
        try:
            movie_data = {
                'rank_today': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[1]').text),
                'rank_yesterday': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[2]').text),
                'name': driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[3]').text,
                'today_revenue': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[4]').text.replace('$', '').replace(',', '')),
                'gross_change_per_day': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[5]').text.replace('$', '').replace(',', '')),
                'gross_change_per_week': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[6]').text.replace('$', '').replace(',', '')),
                'num_of_theaters': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[7]').text),
                'avg_revenue_per_theater': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[8]').text.replace('$', '').replace(',', '')),
                'total_revenue': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[9]').text.replace('$', '').replace(',', '')),
                'total_day': str(driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[10]').text),
                'distributor': driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i + 2}]/td[11]').text,
            }

            movie_lists.append(Movie(**movie_data))  # Unpacking the dictionary
            i += 1
        except Exception as e:
            break

    # Quit Chrome driver
    driver.quit()

    return movie_lists


def create_csv_data(movies):
    output = io.StringIO()
    writer = csv.writer(output)
    # Ghi tiêu đề cột
    writer.writerow(Movie.__annotations__.keys())
    # Ghi dữ liệu
    for movie in movies:
        writer.writerow(movie.__dict__.values())
    return output.getvalue()
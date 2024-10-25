import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from datetime import datetime
from src.anhnm1135.utils.cafef_urls import cafef_urls
import re


def extract_content_keywords(url):
  response = requests.get(url)
  tree = html.fromstring(response.content)
  title = tree.xpath('//title/text()')
  description = tree.xpath('//meta[@name="description"]/@content')
  keywords = tree.xpath('//meta[@name="keywords"]/@content')
  author = tree.xpath('//meta[@property="article:author"]/@content')
  return title, description, keywords, author


def extract_raw_content(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  paragraphs = soup.find_all('p')
  content = " ".join([p.text for p in paragraphs])
  return content

class Cleansed():
   def cafef_content(content):
      content = content.replace("|", "").replace("\n", "").replace("MỚI NHẤT!", "")
      if pd.isna(content):
          return content
      # xoa dau
      match1 = re.search(r'AM|PM', content)
      if match1:
          # Tìm vị trí bắt đầu của "AM" hoặc "PM"
          index = match1.start()
          # Loại bỏ dữ liệu từ đầu đến từ khóa "AM" hoặc "PM"
          content_cleaned = content[index + len(match1.group()):].strip()
          content = content_cleaned
      
      # xoa cuoi 
      remove2 = content.split('Địa chỉ: Tầng 21 Tòa nhà Center Building.')[:-1]
      content = ''.join(remove2)
      
      return content


def crawler_cafef_topic(url):
    topic = url.split("/")[-1].replace(".chn", "").replace('-', '_')

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('div', class_='tlitem')

    article_data = []

    for article in articles:
        title = article.find('a').text.strip()
        url_article = "https://cafef.vn" + article.find('a')['href']
        article_response = requests.get(url_article)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        if article_soup.find('span', class_='pdate'):
            publish_time = article_soup.find('span', class_='pdate').text.strip() 
        
            date_part_formatted = datetime.strptime(publish_time, '%d-%m-%Y - %H:%M %p').strftime('%Y-%m-%d')
            # date_part, time_part = publish_time.split(" - ")
            # date_part_formatted = datetime.strptime(date_part, '%d-%m-%Y').strftime('%Y-%m-%d')

            content = Cleansed.cafef_content(extract_raw_content(url = url_article))

            _, description, keywords, author = extract_content_keywords(url = url_article)

            article_data.append({
                'topic' : topic, 
                'title': title,
                'URL': url_article,
                'publish Time': publish_time,
                'description': description, 
                'keywords': keywords, 
                'author': author,
                'content': content, 
                'cob_dt' : date_part_formatted
            })
        else:
           print("No publish date found! =>> skip")

    # Chuyển danh sách thành DataFrame để dễ làm việc
    df = pd.DataFrame(article_data)
    return df

def crawler_cafef():
   df_cafef = pd.DataFrame(columns=['topic', 'title', 'URL', 'publish Time', 'description', 
                           'keywords', 'author', 'content', 'cob_dt'])
   for url in cafef_urls:
      df_topic = crawler_cafef_topic(url = url)
      # df_topic = df_topic[df_topic['cob_dt'] == 'execution_date'] ### chon ngay hien tai
      df_cafef = pd.concat([df_cafef, df_topic], ignore_index=True)

   return df_cafef
      
   
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# from lxml import html
# from datetime import datetime
# from src.anhnm1135.utils.cafef_urls import cafef_urls
# import re


# def extract_content_keywords(url):
#   response = requests.get(url)
#   tree = html.fromstring(response.content)
#   title = tree.xpath('//title/text()')
#   description = tree.xpath('//meta[@name="description"]/@content')
#   keywords = tree.xpath('//meta[@name="keywords"]/@content')
#   author = tree.xpath('//meta[@property="article:author"]/@content')
#   return title, description, keywords, author


# def extract_raw_content(url):
#   response = requests.get(url)
#   soup = BeautifulSoup(response.content, 'html.parser')
#   paragraphs = soup.find_all('p')
#   content = " ".join([p.text for p in paragraphs])
#   return content

# class Cleansed():
#    def cafef_content(content):
#       content = content.replace("|", "").replace("\n", "").replace("MỚI NHẤT!", "")
#       if pd.isna(content):
#           return content
#       # xoa dau
#       match1 = re.search(r'AM|PM', content)
#       if match1:
#           # Tìm vị trí bắt đầu của "AM" hoặc "PM"
#           index = match1.start()
#           # Loại bỏ dữ liệu từ đầu đến từ khóa "AM" hoặc "PM"
#           content_cleaned = content[index + len(match1.group()):].strip()
#           content = content_cleaned
      
#       # xoa cuoi 
#       remove2 = content.split('Địa chỉ: Tầng 21 Tòa nhà Center Building.')[:-1]
#       content = ''.join(remove2)
      
#       return content


# def crawler_cafef_topic(url):
#     topic = url.split("/")[-1].replace(".chn", "").replace('-', '_')

#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     articles = soup.find_all('div', class_='tlitem')

#     article_data = []

#     for article in articles:
#         title = article.find('a').text.strip()
#         url_article = "https://cafef.vn" + article.find('a')['href']
#         article_response = requests.get(url_article)
#         article_soup = BeautifulSoup(article_response.content, 'html.parser')

#         publish_time = article_soup.find('span', class_='pdate').text.strip() if article_soup.find('span', class_='pdate') else 'No date available'
#         date_part = datetime.strptime(publish_time, '%d-%m-%Y - %H:%M %p')
#         # date_part, time_part = publish_time.split(" - ")
#         date_part_formatted = datetime.strptime(date_part, '%d-%m-%Y').strftime('%Y-%m-%d')

#         content = Cleansed.cafef_content(extract_raw_content(url = url_article))

#         _, description, keywords, author = extract_content_keywords(url = url_article)

#         article_data.append({
#             'topic' : topic, 
#             'title': title,
#             'URL': url_article,
#             'publish Time': publish_time,
#             'description': description, 
#             'keywords': keywords, 
#             'author': author,
#             'content': content, 
#             'cob_dt' : date_part_formatted
#         })

#     # Chuyển danh sách thành DataFrame để dễ làm việc
#     df = pd.DataFrame(article_data)
#     return df

# def crawler_cafef():
#    df_cafef = pd.DataFrame(columns=['topic', 'title', 'URL', 'publish Time', 'description', 
#                            'keywords', 'author', 'content', 'cob_dt'])
#    for url in cafef_urls:
#       df_topic = crawler_cafef_topic(url = url)
#       # df_topic = df_topic[df_topic['cob_dt'] == 'execution_date'] ### chon ngay hien tai
#       df_cafef = pd.concat([df_cafef, df_topic], ignore_index=True)

#    return df_cafef
      
   
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import psycopg2
from tqdm import tqdm
import os
import requests
from lxml import html
from dotenv import load_dotenv
from datetime import datetime
import re


load_dotenv()

# PostgreSQL 연결 정보 설정
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


def clean_timestamp_format(timestamp):
    if timestamp.endswith(':00'):
        return timestamp[:-3]  # :00 제거
    return timestamp

# DB 연결
def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

# DB 연결을 한 번만 열어서 여러 번 사용하도록 개선
def get_cursor():
    conn = get_db_connection()
    cursor = conn.cursor()
    return conn, cursor

# Selenium WebDriver 설정
def get_driver():
    # Chrome 옵션 설정
    options = Options()
    options.add_argument('--headless')  # GUI 없이 실행
    options.add_argument('--no-sandbox')  # 일부 서버 환경에서 필요
    options.add_argument('--disable-dev-shm-usage')  # 리소스 최적화

    # ChromeDriver 실행
    driver = webdriver.Chrome(options=options)
    return driver


# 뉴스 크롤링 함수
def crawl_news():
    # 드라이버 시작
    driver = get_driver()
    driver.get("https://news.naver.com/main/ranking/popularDay.naver")
    time.sleep(3)  # 페이지가 로드될 때까지 잠시 대기

    # 언론사 뉴스 링크들 가져오기
    news_links = []

    # # div[1~7]과 div[1~12] 반복 처리
    for i in range(1, 8):
        for j in range(1, 13):
            try:
                xpath = f'//*[@id="wrap"]/div[4]/div[2]/div[{i}]/div[{j}]/a'
                link_element = driver.find_element(By.XPATH, xpath)
                news_links.append(link_element.get_attribute('href'))
            except:
                pass  # 해당 링크가 없으면 넘어감

            # "다른 언론사 랭킹 더보기" 버튼 클릭하여 추가 데이터 로드
            try:
                more_button = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/button')
                more_button.click()
                time.sleep(3)  # 버튼 클릭 후 페이지가 로드될 때까지 대기
            except:
                pass  # 더 이상 버튼이 없으면 그냥 진행

    # # 다시 한번 링크 추출
    # for i in range(1, 8):
    #     for j in range(1, 13):
    #         try:
    #             xpath = f'//*[@id="wrap"]/div[4]/div[2]/div[{i}]/div[{j}]/a'
    #             link_element = driver.find_element(By.XPATH, xpath)
    #             news_links.append(link_element.get_attribute('href'))
    #         except:
    #             pass  # 해당 링크가 없으면 넘어감
    # print(news_links)
    print(f"기사 링크 수집 완료: {len(news_links)}개")
    # news_links = ['https://media.naver.com/press/018/ranking?type=popular']
    # DB 연결
    conn, cursor = get_cursor()

    # 각 뉴스 링크를 순차적으로 방문하여 해당 페이지의 기사 링크들 추출
    for news_url in tqdm(news_links):
        driver.get(news_url)
        time.sleep(2)  # 페이지 로드 대기

        # 뉴스 링크들 추출 (기사 리스트)
        article_links = []
        for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
            try:
                article_xpath = f'//*[@id="ct"]/div[2]/div[2]/ul/li[{i}]/a'
                article_element = driver.find_element(By.XPATH, article_xpath)
                article_links.append(article_element.get_attribute('href'))
            except:
                pass  # 해당 기사 링크가 없으면 넘어감

        for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
            try:
                article_xpath = f'//*[@id="ct"]/div[2]/div[3]/ul/li[{i}]/a'
                article_element = driver.find_element(By.XPATH, article_xpath)
                article_links.append(article_element.get_attribute('href'))
            except:
                pass  # 해당 기사 링크가 없으면 넘어감

        print(f"{len(article_links)}개의 기사 링크 수집 완료")

        # 각 기사 페이지 방문하여 필요한 데이터 추출
        for article_url in article_links:
            # lxml로 HTML 파싱
            response = requests.get(article_url)
            tree = html.fromstring(response.content)

            # 뉴스 제목, 작성자, 본문, 발행일 등 정보 추출
            try:
                title = tree.xpath('//*[@id="title_area"]/span/text()')[0].strip()
            except:
                title = None

            try:
                writer = tree.xpath('//*[@id="ct"]/div[1]/div[3]/div[2]/a/em/text()')[0].strip()
            except:
                writer = None

            content = ""
            try:
                content_parts = tree.xpath('//*[@id="dic_area"]//text()')
                content = " ".join([part.strip() for part in content_parts if part.strip()])
            except:
                content = None

            try:
                published_date = tree.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div/span/@data-date-time')[0].strip()
            except:
                published_date = None

            # 카테고리 ID 추출
            category_id = None
            try:
                category = tree.xpath('//*[@aria-selected="true"]/span[@class="Nitem_link_menu"]/text()')[0].strip()
                category_dict = {'경제': 1, '정치': 2, '사회': 3, '생활': 4, '세계': 5, 'IT': 6}
                category_id = category_dict.get(category, None)
            except:
                category_id = None

            # 미디어 회사 ID 추출
            media_company_id = None
            try:
                # company_name = tree.xpath('//*[@id="_OFFICE_HEADER_TITLE"]/a/span/text()')[0].strip()
                # cursor.execute("SELECT company_id FROM news_mediacompany WHERE name = %s", (company_name,))
                # result = cursor.fetchone()
                # if result:
                #     media_company_id = result[0]
                media_company_id = int(article_url.split("/")[4])
            except:
                media_company_id = None

            article_id = None
            try:
                article_id = article_url.split("/")[5]
                article_id = article_id.split('?')[0]
            except:
                article_id = None

            summary = None
            sentiment_score = None
            published_date = clean_timestamp_format(published_date)
            print(f"{title, writer, content, summary, published_date, sentiment_score, category_id, media_company_id, article_url, article_id}")
            # print(f"{published_date}")
            cursor.execute("""
                    INSERT INTO news_news (title, writer, content, summary, published_date, sentiment_score, category_id, media_company_id, article_id, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
            title, writer, content, summary, published_date, sentiment_score, category_id, media_company_id,
            article_id, article_url))

        conn.commit()
    conn.close()  # DB 연결 종료
    driver.quit()  # 드라이버 종료


if __name__ == "__main__":
    crawl_news()



# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time
# import psycopg2
# from tqdm import tqdm
# import os
# from dotenv import load_dotenv
#
#
# load_dotenv()
#
# # PostgreSQL 연결 정보 설정
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")
#
# # DB 연결
# def get_db_connection():
#     return psycopg2.connect(
#         host=POSTGRES_HOST,
#         database=POSTGRES_DB,
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD
#     )
#
# # DB 연결을 한 번만 열어서 여러 번 사용하도록 개선
# def get_cursor():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     return conn, cursor
#
# # Selenium WebDriver 설정
# def get_driver():
#     # Chrome 옵션 설정
#     options = Options()
#     options.add_argument('--headless')  # GUI 없이 실행
#     options.add_argument('--no-sandbox')  # 일부 서버 환경에서 필요
#     options.add_argument('--disable-dev-shm-usage')  # 리소스 최적화
#
#     # ChromeDriver 실행
#     driver = webdriver.Chrome(options=options)
#     return driver
#
#
# # 뉴스 크롤링 함수
# def crawl_news():
#     # 드라이버 시작
#     driver = get_driver()
#     driver.get("https://news.naver.com/main/ranking/popularDay.naver")
#     time.sleep(3)  # 페이지가 로드될 때까지 잠시 대기
#
#     # 언론사 뉴스 링크들 가져오기
#     news_links = []
#
#     # div[1~7]과 div[1~12] 반복 처리
#     for i in range(1, 8):
#         for j in range(1, 13):
#             try:
#                 xpath = f'//*[@id="wrap"]/div[4]/div[2]/div[{i}]/div[{j}]/a'
#                 link_element = driver.find_element(By.XPATH, xpath)
#                 news_links.append(link_element.get_attribute('href'))
#             except:
#                 pass  # 해당 링크가 없으면 넘어감
#
#             # "다른 언론사 랭킹 더보기" 버튼 클릭하여 추가 데이터 로드
#             try:
#                 more_button = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/button')
#                 more_button.click()
#                 time.sleep(3)  # 버튼 클릭 후 페이지가 로드될 때까지 대기
#             except:
#                 pass  # 더 이상 버튼이 없으면 그냥 진행
#
#     # # 다시 한번 링크 추출
#     # for i in range(1, 8):
#     #     for j in range(1, 13):
#     #         try:
#     #             xpath = f'//*[@id="wrap"]/div[4]/div[2]/div[{i}]/div[{j}]/a'
#     #             link_element = driver.find_element(By.XPATH, xpath)
#     #             news_links.append(link_element.get_attribute('href'))
#     #         except:
#     #             pass  # 해당 링크가 없으면 넘어감
#     print(news_links)
#     print(f"기사 링크 수집 완료: {len(news_links)}개")
#
#     # DB 연결
#     conn, cursor = get_cursor()
#
#     # 각 뉴스 링크를 순차적으로 방문하여 해당 페이지의 기사 링크들 추출
#     for news_url in tqdm(news_links):
#         driver.get(news_url)
#         time.sleep(2)  # 페이지 로드 대기
#
#         # 뉴스 링크들 추출 (기사 리스트)
#         article_links = []
#         for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
#             try:
#                 article_xpath = f'//*[@id="ct"]/div[2]/div[2]/ul/li[{i}]/a'
#                 article_element = driver.find_element(By.XPATH, article_xpath)
#                 article_links.append(article_element.get_attribute('href'))
#             except:
#                 pass  # 해당 기사 링크가 없으면 넘어감
#
#         for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
#             try:
#                 article_xpath = f'//*[@id="ct"]/div[2]/div[3]/ul/li[{i}]/a'
#                 article_element = driver.find_element(By.XPATH, article_xpath)
#                 article_links.append(article_element.get_attribute('href'))
#             except:
#                 pass  # 해당 기사 링크가 없으면 넘어감
#
#         print(f"{len(article_links)}개의 기사 링크 수집 완료")
#
#         # 각 기사 페이지 방문하여 필요한 데이터 추출
#         for article_url in article_links:
#             driver.get(article_url)
#             time.sleep(2)  # 페이지 로드 대기
#
#             # 뉴스 제목, 작성자, 본문, 발행일 등 정보 추출
#             try:
#                 title = driver.find_element(By.XPATH, '//*[@id="title_area"]/span').text
#             except:
#                 title = None
#
#             try:
#                 writer = driver.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[3]/div[2]/a/em').text
#             except:
#                 writer = None
#
#             content = ""
#             try:
#                 content_parts = driver.find_elements(By.XPATH, '//*[@id="dic_area"]/text()')
#                 content = " ".join([part.text.strip() for part in content_parts if part.text.strip()])
#             except:
#                 content = None
#
#             try:
#                 published_date = driver.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[3]/div[1]/div[1]/span').text
#             except:
#                 published_date = None
#
#             # 카테고리 ID 추출
#             category_id = None
#             try:
#                 category = driver.find_element(By.XPATH, '//*[@aria-selected="true"]/span[@class="Nitem_link_menu"]').text
#                 category_dict = {'경제': 1, '정치': 2, '사회': 3, '생활': 4, '세계': 5, 'IT': 6}
#                 category_id = category_dict.get(category, None)
#             except:
#                 category_id = None
#
#             # 미디어 회사 ID 추출
#             media_company_id = None
#             try:
#                 company_name = driver.find_element(By.XPATH, '//*[@id="_OFFICE_HEADER_TITLE"]/a/span').text
#                 cursor.execute("SELECT company_id FROM news_mediacompany WHERE name = %s", (company_name,))
#                 result = cursor.fetchone()
#                 if result:
#                     media_company_id = result[0]
#             except:
#                 media_company_id = None
#
#             # print(f"{title, writer, content, published_date, category_id, media_company_id, article_url}")
#             print(content)
#             exit()
#             # DB에 데이터 삽입
#             if title and writer and content and published_date:
#                 cursor.execute("""
#                         INSERT INTO news_news (title, writer, content, summary, published_date, sentiment_score, category_id, media_company_id)
#                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                     """, (title, writer, content, "", published_date, None, category_id, media_company_id))
#                 conn.commit()
#
#     conn.close()  # DB 연결 종료
#     driver.quit()  # 드라이버 종료
#
#
# if __name__ == "__main__":
#     crawl_news()
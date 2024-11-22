# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time
# import psycopg2
# from tqdm import tqdm
# import os
# import requests
# from lxml import html
# from dotenv import load_dotenv
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from datetime import datetime
# import re
# from spark_processor import generate_summary, analyze_sentiment, extract_keywords
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
#
# def clean_timestamp_format(timestamp):
#     if timestamp.endswith(':00'):
#         return timestamp[:-3]  # :00 제거
#     return timestamp
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
# def crawl_news():
#     # PostgreSQL에서 company_id 읽어오기
#     conn, cursor = get_cursor()
#     cursor.execute("SELECT company_id FROM news_mediacompany")
#     company_ids = [str(row[0]).zfill(3) for row in cursor.fetchall() if str(row[0]).zfill(3) != "000"]  # company_id를 항상 3자리로 포맷
#
#     # 링크 생성
#     base_url = "https://media.naver.com/press/{}/ranking?type=popular"
#     news_links = [base_url.format(company_id) for company_id in company_ids]
#     # print(news_links)
#     print(f"생성된 뉴스 링크 수: {len(news_links)}")
#
#     cursor.close()
#     conn.close()
#     # news_links = ['https://media.naver.com/press/006/ranking?type=popular']
#
#     # Selenium WebDriver 시작
#     driver = get_driver()
#
#     # 기존 기사 ID 확인
#     conn, cursor = get_cursor()
#     cursor.execute("SELECT url FROM news_news")
#     existing_article_ids = set(row[0] for row in cursor.fetchall())  # 이미 저장된 article_id
#     print(f"이미 저장된 기사 수: {len(existing_article_ids)}")
#     # print(existing_article_ids)
#     # exit()
#     # 각 뉴스 링크를 순차적으로 방문하여 해당 페이지의 기사 링크들 추출
#     batch = []  # 기사 데이터를 저장할 배치 리스트
#     article_links = []
#     for news_url in tqdm(news_links):
#         driver.get(news_url)
#
#         # 명시적 대기: 페이지가 완전히 로드될 때까지 기다림
#         wait = WebDriverWait(driver, 10)
#         wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ct"]/div[2]/div[2]/ul/li[1]/a')))  # 첫 번째 기사 링크가 로드될 때까지 기다림
#
#         # 뉴스 링크들 추출 (기사 리스트)
#         for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
#             try:
#                 article_xpath = f'//*[@id="ct"]/div[2]/div[2]/ul/li[{i}]/a'
#                 article_element = driver.find_element(By.XPATH, article_xpath)
#                 if article_element.get_attribute('href') not in existing_article_ids:
#                     article_links.append(article_element.get_attribute('href'))
#             except:
#                 pass  # 해당 기사 링크가 없으면 넘어감
#
#         for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
#             try:
#                 article_xpath = f'//*[@id="ct"]/div[2]/div[3]/ul/li[{i}]/a'
#                 article_element = driver.find_element(By.XPATH, article_xpath)
#                 if article_element.get_attribute('href') not in existing_article_ids:
#                     article_links.append(article_element.get_attribute('href'))
#             except:
#                 pass  # 해당 기사 링크가 없으면 넘어감
#
#         # print(article_links)
#         print(f"{len(article_links)}개의 기사 링크 수집 완료")
#         # exit()
#         # 각 기사 페이지 방문하여 필요한 데이터 추출
#     for article_url in article_links:
#         # lxml로 HTML 파싱
#         response = requests.get(article_url)
#         tree = html.fromstring(response.content)
#
#         # 뉴스 제목, 작성자, 본문, 발행일 등 정보 추출
#         try:
#             article_id = article_url.split("/")[5].split('?')[0]
#             # if article_id in existing_article_ids:
#             #     print(f"이미 저장된 기사입니다: {article_id}")
#             #     continue
#         except:
#             # print("기사 ID 추출 실패")
#             # continue
#             article_id = None
#         try:
#             title = tree.xpath('//*[@id="title_area"]/span/text()')[0].strip()
#         except:
#             title = None
#
#         try:
#             writer = tree.xpath('//*[@id="ct"]/div[1]/div[3]/div[2]/a/em/text()')[0].strip()
#         except:
#             writer = None
#
#         content = ""
#         try:
#             content_parts = tree.xpath('//*[@id="dic_area"]//text()')
#             content = " ".join([part.strip() for part in content_parts if part.strip()])
#         except:
#             content = None
#
#         try:
#             published_date = tree.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div/span/@data-date-time')[0].strip()
#             published_date = clean_timestamp_format(published_date)
#         except:
#             published_date = None
#
#         # 카테고리 ID 추출
#         category_id = None
#         try:
#             category = tree.xpath('//*[@aria-selected="true"]/span[@class="Nitem_link_menu"]/text()')[0].strip()
#             category_dict = {'경제': 1, '정치': 2, '사회': 3, '생활': 4, '세계': 5, 'IT': 6}
#             if category not in ['경제', '정치', '사회', '생활', '세계', 'IT']:
#                 continue
#             category_id = category_dict.get(category, None)
#         except:
#             category_id = None
#
#         # # 미디어 회사 ID 추출
#         try:
#             media_company_id = int(article_url.split("/")[4])  # 회사 ID 추출
#             cursor.execute("SELECT COUNT(*) FROM news_mediacompany WHERE company_id = %s", (media_company_id,))
#             company_exists = cursor.fetchone()[0]
#             if not company_exists:
#                 raise ValueError(f"Invalid media_company_id: {media_company_id}")
#         except Exception as e:
#             print(f"Media company ID validation failed: {e}")
#             media_company_id = None
#
#         summary = generate_summary(content) if content else None
#         sentiment_score = analyze_sentiment(content) if content else None
#         keywords = extract_keywords(content) if content else None
#         # print("본문:", content)
#         # print("요약:", summary)
#         # print(f"{title, writer, content, summary, published_date, sentiment_score, category_id,media_company_id, article_id, article_url, keywords}")
#         # exit()
#         # 배치에 기사 추가
#         batch.append((
#             title, writer, content, summary, published_date, sentiment_score, category_id,
#             media_company_id, article_id, article_url, keywords
#         ))
#
#         print(len(batch))
#         # print_mediacompany_table(media_company_id)
#         # 배치가 20개가 되면 DB에 저장
#         if len(batch) == 50:
#             cursor.executemany("""
#                 INSERT INTO news_news (title, writer, content, summary, published_date, sentiment_score,
#                                        category_id, media_company_id, article_id, url, keyword)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, batch)
#             conn.commit()
#             print(f"{len(batch)}개 기사를 데이터베이스에 저장 완료")
#             batch.clear()  # 배치 초기화
#     if len(batch) >= 1:
#         cursor.executemany("""
#             INSERT INTO news_news (title, writer, content, summary, published_date, sentiment_score,
#                                    category_id, media_company_id, article_id, url, keyword)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """, batch)
#         conn.commit()
#         print(f"{len(batch)}개 기사를 데이터베이스에 저장 완료")
#         batch.clear()  # 배치 초기화
#
#     conn.close()  # DB 연결 종료
#     driver.quit()  # 드라이버 종료
#
#
# # def print_mediacompany_table(num):
# #     conn, cursor = get_cursor()
# #
# #     # news_mediacompany 테이블에서 모든 데이터 조회
# #     cursor.execute("SELECT * FROM news_mediacompany")
# #
# #     # 결과 가져오기
# #     rows = cursor.fetchall()
# #
# #     # 각 행을 출력
# #     for row in rows:
# #         if row[2] == num:
# #             print(row)
# #
# #
# #     # DB 연결 종료
# #     cursor.close()
# #     conn.close()
#
#
# if __name__ == "__main__":
#     crawl_news()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os
import requests
from lxml import html
from dotenv import load_dotenv
from tqdm import tqdm
from datetime import datetime
from spark_processor import generate_summary, analyze_sentiment, extract_keywords
from pyspark.sql import SparkSession

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


def crawl_news():
    # PostgreSQL에서 company_id 읽어오기
    conn, cursor = get_cursor()
    cursor.execute("SELECT company_id FROM news_mediacompany")
    company_ids = [str(row[0]).zfill(3) for row in cursor.fetchall() if str(row[0]).zfill(3) != "000"]  # company_id를 항상 3자리로 포맷

    # 링크 생성
    base_url = "https://media.naver.com/press/{}/ranking?type=popular"
    news_links = [base_url.format(company_id) for company_id in company_ids]
    print(f"생성된 뉴스 링크 수: {len(news_links)}")

    cursor.close()
    conn.close()
    # news_links = ['https://media.naver.com/press/056/ranking?type=popular']

    # Selenium WebDriver 시작
    driver = get_driver()

    # 기존 기사 ID 확인
    conn, cursor = get_cursor()
    cursor.execute("SELECT url FROM news_news")
    existing_article_ids = set(row[0] for row in cursor.fetchall())  # 이미 저장된 article_id
    print(f"이미 저장된 기사 수: {len(existing_article_ids)}")
    # exit()

    article_links = []
    for news_url in tqdm(news_links):
        driver.get(news_url)

        # 명시적 대기: 페이지가 완전히 로드될 때까지 기다림
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ct"]/div[2]/div[2]/ul/li[1]/a')))  # 첫 번째 기사 링크가 로드될 때까지 기다림

        # 뉴스 링크들 추출 (기사 리스트)
        for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
            try:
                article_xpath = f'//*[@id="ct"]/div[2]/div[2]/ul/li[{i}]/a'
                article_element = driver.find_element(By.XPATH, article_xpath)
                if article_element.get_attribute('href') not in existing_article_ids:
                    article_links.append(article_element.get_attribute('href'))
            except:
                pass

        for i in range(1, 11):  # 각 뉴스 페이지에서 1~10번째 기사 링크
            try:
                article_xpath = f'//*[@id="ct"]/div[2]/div[3]/ul/li[{i}]/a'
                article_element = driver.find_element(By.XPATH, article_xpath)
                if article_element.get_attribute('href') not in existing_article_ids:
                    article_links.append(article_element.get_attribute('href'))
            except:
                pass

        print(f"{len(article_links)}개의 기사 링크 수집 완료")

    # Spark 세션 생성
    spark = SparkSession.builder.appName("NewsCrawl").getOrCreate()

    batch = []  # 기사 데이터를 저장할 배치 리스트
    for article_url in article_links:
        response = requests.get(article_url)
        tree = html.fromstring(response.content)

        try:
            article_id = article_url.split("/")[5].split('?')[0]
        except:
            article_id = None

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
            published_date = clean_timestamp_format(published_date)
        except:
            published_date = None

        category_id = None
        try:
            category = tree.xpath('//*[@aria-selected="true"]/span[@class="Nitem_link_menu"]/text()')[0].strip()
            category_dict = {'경제': 1, '정치': 2, '사회': 3, '생활': 4, '세계': 5, 'IT': 6}
            if category not in ['경제', '정치', '사회', '생활', '세계', 'IT']:
                continue
            category_id = category_dict.get(category, None)
        except:
            category_id = None

        if category_id == None:
            continue

        media_company_id = None
        try:
            media_company_id = int(article_url.split("/")[4])  # 회사 ID 추출
        except:
            media_company_id = None

        # Spark 처리
        summary = generate_summary(content) if content else None
        sentiment_score = analyze_sentiment(content) if content else None
        keywords = extract_keywords(content) if content else None

        batch.append((title, writer, content, summary, published_date, sentiment_score, category_id,
                      media_company_id, article_id, article_url, keywords))

        print("batch에 저장된 기사 수 :", len(batch))

        if len(batch) == 40:
            # Spark에서 데이터를 DataFrame으로 변환
            df = spark.createDataFrame(batch, ["title", "writer", "content", "summary", "published_date",
                                              "sentiment_score", "category_id", "media_company_id", "article_id", "url", "keyword"])

            # DataFrame 처리 (예: 필터링, 변환 등)
            df.show()

            # DB에 데이터 저장
            conn, cursor = get_cursor()
            for row in batch:
                cursor.execute("""
                    INSERT INTO news_news (title, writer, content, summary, published_date, sentiment_score,
                                           category_id, media_company_id, article_id, url, keyword)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, row)
            conn.commit()

            print(f"{len(batch)}개 기사를 데이터베이스에 저장 완료")
            batch.clear()

    if len(batch) >= 1:
        # Spark에서 데이터를 DataFrame으로 변환
        df = spark.createDataFrame(batch, ["title", "writer", "content", "summary", "published_date",
                                           "sentiment_score", "category_id", "media_company_id", "article_id", "url",
                                           "keyword"])

        # DataFrame 처리 (예: 필터링, 변환 등)
        df.show()

        # DB에 데이터 저장
        conn, cursor = get_cursor()
        for row in batch:
            cursor.execute("""
                INSERT INTO news_news (title, writer, content, summary, published_date, sentiment_score,
                                       category_id, media_company_id, article_id, url, keyword)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, row)
        conn.commit()

        print(f"{len(batch)}개 기사를 데이터베이스에 저장 완료")
        batch.clear()

    conn.close()
    driver.quit()


if __name__ == "__main__":
    crawl_news()

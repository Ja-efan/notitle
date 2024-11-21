from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL 연결 정보 설정
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# PostgreSQL 연결 설정
db_config = {
    "dbname": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
}

# news_mediacompany 테이블에 데이터 추가하는 함수
def insert_into_db(company_id, name):
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO news_mediacompany (company_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
            (company_id, name),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

def get_driver():
    # Chrome 옵션 설정
    options = Options()
    options.add_argument('--headless')  # GUI 없이 실행
    options.add_argument('--no-sandbox')  # 일부 서버 환경에서 필요
    options.add_argument('--disable-dev-shm-usage')  # 리소스 최적화

    # ChromeDriver 실행
    driver = webdriver.Chrome(options=options)
    return driver

# Selenium WebDriver 설정
driver = get_driver()  # ChromeDriver 경로가 환경 변수에 등록되어 있어야 함
driver.get("https://news.naver.com/main/ranking/popularDay.naver")
time.sleep(3)

# 스크롤을 통해 모든 페이지 로드
while True:
    try:
        load_more_button = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/button')
        ActionChains(driver).move_to_element(load_more_button).click().perform()
        time.sleep(2)
    except Exception as e:
        print("No more pages to load.")
        break

# 각 언론사별 데이터를 수집
for i in range(1, 8):  # div[1~7]
    for j in range(1, 13):  # div[1~12]
        try:
            # 언론사 링크 클릭
            link_xpath = f'//*[@id="wrap"]/div[4]/div[2]/div[{i}]/div[{j}]/a'
            media_link = driver.find_element(By.XPATH, link_xpath)
            media_url = media_link.get_attribute("href")
            driver.execute_script("window.open(arguments[0]);", media_url)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)

            # 언론사 ID 및 이름 수집
            company_id = media_url.split("/")[4]
            company_name = driver.find_element(
                By.XPATH,
                '/html/body/div[2]/div/section[1]/header/div[4]/div/div[2]/div[1]/div/h3/a'
            ).text

            # 데이터베이스에 저장
            insert_into_db(company_id, company_name)
            print(f"Added {company_name} with ID {company_id} to database.")

            # 탭 닫기
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f"Error processing div[{i}]/div[{j}]: {e}")
            continue

# Selenium 드라이버 종료
driver.quit()



####----------------------------------------------------------------------------------------------------------------------
####----------------------------------------------------------------------------------------------------------------------
### 추후에 news_mediacompany table 맨 위에 있는 연합뉴스,0 삭제 코드 (더미 데이터임)
# import psycopg2
#
# # PostgreSQL DB에 연결
# conn = psycopg2.connect(dbname="NewsDatabase", user="postgres", password="skadnwoghks", host="postgres-server")
# cursor = conn.cursor()
#
# # 삭제 쿼리 실행
# delete_query = """
# DELETE FROM news_mediacompany
# WHERE name = '연합뉴스' AND company_id = 0;
# """
# cursor.execute(delete_query)
#
# # 변경사항 커밋
# conn.commit()
#
# # 연결 종료
# cursor.close()
# conn.close()
#
# print("연합뉴스, 0 데이터가 삭제되었습니다.")
####----------------------------------------------------------------------------------------------------------------------
####----------------------------------------------------------------------------------------------------------------------



####----------------------------------------------------------------------------------------------------------------------
####----------------------------------------------------------------------------------------------------------------------
### news_category table에 관련 데이터 삽입'
# import psycopg2
#
# # PostgreSQL DB에 연결
# conn = psycopg2.connect(dbname="NewsDatabase", user="postgres", password="skadnwoghks", host="postgres-server")
# cursor = conn.cursor()
#
# # news_category 테이블에 데이터 삽입
# insert_query = """
# INSERT INTO news_category (category_name)
# VALUES
#     ('정치'),
#     ('사회'),
#     ('생활'),
#     ('세계'),
#     ('IT');
# """
# cursor.execute(insert_query)
#
# # 변경사항 커밋
# conn.commit()
#
# # 연결 종료
# cursor.close()
# conn.close()
#
# print("news_category 테이블에 데이터가 삽입되었습니다.")
####----------------------------------------------------------------------------------------------------------------------
####----------------------------------------------------------------------------------------------------------------------
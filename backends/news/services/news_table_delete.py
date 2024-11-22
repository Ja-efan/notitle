import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL 연결 정보 설정
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


# PostgreSQL DB에 연결
try:
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,    # 데이터베이스 이름
        user=POSTGRES_USER,    # 사용자 이름
        password=POSTGRES_PASSWORD,# 비밀번호
        host=POSTGRES_HOST,        # 호스트 (로컬은 'localhost')
        port=POSTGRES_PORT         # 포트 (기본값: 5432)
    )
    cursor = conn.cursor()
    print("데이터베이스에 성공적으로 연결되었습니다.")

    # news_news 테이블 데이터 삭제 쿼리
    delete_query = "DELETE FROM news_news;"
    cursor.execute(delete_query)

    # 변경사항 커밋
    conn.commit()
    print("news_news 테이블의 데이터가 삭제되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")
finally:
    # 연결 종료
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        print("데이터베이스 연결이 종료되었습니다.")
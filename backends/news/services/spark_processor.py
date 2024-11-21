import os
import json 
import openai
from openai import OpenAI
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, lit
from pyspark.sql.types import StringType, FloatType
import requests
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL 연결 정보 설정 
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# PostgreSQL 테이블 이름 
# POSTGRES_TABLE = 'news_news'
SOURCE_TABLE = "news_news"
TARGET_TABLE = "news_news"

# OpenAI 
CHAT_MODEL = "gpt-4o-mini"

# Spark 
WRITE_MODE = "overwrite"  # or 'append'


def initialize_spark_session():
    """
    Spark 세션을 초기화합니다.

    Returns:
        SparkSession: 설정된 Spark 세션 인스턴스 
    """
    return SparkSession.builder.appName("NewsETL").getOrCreate()


def read_from_postgres(spark):
    """
    PosgtresSQL에서 데이터를 읽어옵니다.

    Args:
        spark (SparkSession): 설정이 완료된 Spark 세션 인스턴스
    """
    return spark.read \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}") \
        .option("dbtable", SOURCE_TABLE) \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .load()


def generate_summary(content):
    """
    OpenAI API를 사용하여 텍스트 요약을 생성합니다.

    Args:
        content (str): 뉴스 기사 내용
    """
    client = OpenAI()

    response = client.ChatCompletion.create(
        model = CHAT_MODEL,
        messages=[
            {"role": "system", "content": "다음 텍스트를 2-3문장으로 요약해주세요."},
            {"role": "user", "content": content}
        ],
        max_tokens=100
    )

    summary = response.choices[0].message.content.strip()
    return summary


def analyze_sentiment(content):
    """
    OpenAI API를 사용하여 텍스트의 감정 점수를 분석합니다.

    Args:
        content (str): 기사 내용의 감정 점수 (긍정: 1, 부정: -1)
    """
    client = OpenAI()
    response = client.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "다음 텍스트의 감정 점수를 -1 혹은 1로 반환해주세요. (부정적인 경우: -1, 긍정적인 경우: 1) "},
            {"role": "system", "content": content}
        ],
        max_tokens = 100
    )
    sentiment_score = float(response.choices[0].message.content.strip())

    return sentiment_score


def register_udfs():
    """
    UDF(User Defined Functions)를 등록합니다.
    """
    return {
        "summary": udf(generate_summary, StringType()),
        "sentiment": udf(analyze_sentiment, FloatType())
    }


def process_data(df, udfs):
    """
    데이터를 처리합니다.

    Args:
        df (pd.DataFrame): _description_
        udfs (_type_): _description_
    """
    return df.withColumn("summary", udfs['summary'](col('content')))\
        .withColumn("sentiment_score", udfs['sentiment'](col('content')))


def write_to_postgres(df):
    """
    처리된 데이터를 PostgreSQL에 저장합니다.

    Args:
        df (_type_): _description_
    """
    df.write \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}") \
        .option("dbtable", TARGET_TABLE) \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .mode(WRITE_MODE) \
        .save()


def main():
    """
    ETL 파이프라인의 메인 함수 
    """

    spark = initialize_spark_session()

    # 원본 데이터 읽기
    source_df = read_from_postgres(spark)

    # 변환 udf 등록 
    udfs = register_udfs()

    # 데이터 처리 
    processed_df = process_data(source_df, udfs)

    # 처리된 데이터 저장 
    write_to_postgres(processed_df)


if __name__== '__main__':
    main()
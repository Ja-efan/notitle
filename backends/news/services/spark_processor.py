import os
import json
import openai
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, lit
from pyspark.sql.types import StringType, FloatType
import requests
from dotenv import load_dotenv
import re

load_dotenv()

# PostgreSQL 연결 정보 설정
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# PostgreSQL 테이블 이름
POSTGRES_TABLE = 'news_news'
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
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model = CHAT_MODEL,
        messages=[
            {"role": "system", "content": "다음 텍스트를 2문장으로 짧게 요약해주세요."},
            {"role": "user", "content": content}
        ],
        max_tokens=100
    )

    summary = response.choices[0].message.content.strip()
    # print(f"Generated summary: {summary}")
    return summary


def analyze_sentiment(content):
    """
    OpenAI API를 사용하여 텍스트의 감정 점수를 분석합니다.

    Args:
        content (str): 기사 내용의 감정 점수 (긍정: 1, 부정: -1)
    """
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "다음 텍스트의 감정 점수를 오직 -1 혹은 1로 반환해주세요. 다른 string 붙이지 말고 오직 -1 또는 1만 긍정, 부정이 애매하다면 0으로 줘도 돼.(부정적인 경우: -1, 긍정적인 경우: 1, 애매한 경우 : 0) "},
            {"role": "system", "content": content}
        ],
        max_tokens = 100
    )
    # sentiment_str = response.choices[0].message.content.strip()
    #
    # # 정규 표현식으로 -1 또는 1만 추출
    # match = re.search(r"[-+]1", sentiment_str)
    #
    # if match:
    #     sentiment_score = float(match.group(0))  # 추출된 숫자 (-1 또는 1)만 사용
    # else:
    #     sentiment_score = None  # -1 또는 1이 아니면 None 처리
    sentiment_score = float(response.choices[0].message.content.strip())
    # print(f"Sentiment score: {sentiment_score}")  # Sentiment 출력
    return sentiment_score

def extract_keywords(content):
    """
    OpenAI API를 사용하여 텍스트에서 키워드를 추출합니다.

    Args:
        content (str): 뉴스 기사 내용
    """
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "다음 텍스트에서 중요한 키워드를 5개만 문자열 형태로 추출해주세요. 각각의 키워드 앞에 숫자와 따옴표 붙이지 말고 그냥 ,(콤마)로만 구분해주세요"},
            {"role": "user", "content": content}
        ],
        max_tokens=50
    )

    # 키워드 추출된 결과
    keywords = response.choices[0].message.content.strip()
    # print(f"Extracted keywords: {keywords}")  # Keywords 출력
    return keywords


def register_udfs():
    """
    UDF(User Defined Functions)를 등록합니다.
    """
    return {
        "summary": udf(generate_summary, StringType()),
        "sentiment": udf(analyze_sentiment, FloatType()),
        "keywords": udf(extract_keywords, StringType())  # 키워드 추출 함수 추가
    }


def process_data(df, udfs):
    """
    데이터를 처리합니다.

    Args:
        df (pd.DataFrame): _description_
        udfs (_type_): _description_
    """
    return df.withColumn("summary", udfs['summary'](col('content'))) \
        .withColumn("sentiment_score", udfs['sentiment'](col('content'))) \
        .withColumn("keywords", udfs['keywords'](col('content')))  # 키워드 추출 추가
    # # print("Processing data...")
    # df = df.withColumn("summary", udfs['summary'](col('content'))) \
    #     .withColumn("sentiment_score", udfs['sentiment'](col('content'))) \
    #     .withColumn("keywords", udfs['keywords'](col('content')))  # 키워드 추출 추가
    #
    # # 처리된 데이터 확인
    # df.show(truncate=False)
    # return df


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
    # data = ["도널드 트럼프 미국 대통령 당선인이 교육부 장관으로 지명한 월드레슬링엔터테인먼트(WWE) 공동 설립자 린다 맥마흔의 과거 영상이 재조명되고 있다. "
    #      "트럼프 당선인은 19일(현지시각) SNS 트루스 소셜에 '린다 맥마흔 전 중소기업청장을 교육부 장관 지명자로 알리게 돼 기쁘다'라며 '우리는 교육이 미국에 다시 돌아오도록 할 것이고 린다는 그 노력의 선봉에 설 것'이라고 밝혔다. "
    #      "교육부 장관에 지명된 린다 맥마흔은 트럼프 당선인의 고액 기부자이자 충성파로 꼽힌다. 그는 남편과 함께 WWE를 공동설립하고 최고경영자(CEO)를 지낸 것으로 유명하다. 트럼프 1기 행정부에서는 중소기업청장을 지냈으며, 이번 대선 과정에서도 정권 인수팀 공동 위원장을 맡았다. "
    #      "맥마흔 지명 사실이 알려지자, 각종 SNS에는 그가 과거 WWE 흥행을 위해 '막장' 시나리오를 불사했던 모습이 공유되고 있다. 한 누리꾼은 '새로운 교육부 장관인 어머니 린다 맥마흔을 소개한다'며 맥마흔이 링에 오른 영상을 올렸다. "
    #      "영상을 보면 맥마흔은 딸을 노려보다 뺨을 올려붙인다. 또 다른 장면에서는 반대로 딸이 엄마에게 욕설을 내뱉다 뺨을 내리치고, 맥마흔이 그대로 쓰러진다. 이어진 장면에서는 맥마흔이 아들의 뺨을 때리자 아들이 그를 결박하고, 그 모습을 지켜보던 딸이 맥마흔을 때린다. "
    #      "누리꾼들은 '이건 교육부 장관으로 원했던 인물상이 아니다', '이 나라가 부끄럽다', '더 나빠질 수 없을 것이다' 등의 반응을 보였다. 한편, 맥마흔은 WWE 운영 당시 성 학대 문제를 묵인했다는 의혹도 받고 있다. "
    #      "이는 전직 링보이 5명이 지난달 맥마흔을 상대로 민사소송을 내며 알려졌다. 이들은 WWE의 고위급 직원들로부터 성적 학대를 당하고 있다는 사실을 맥마흔 부부가 알고 있었으면서도 보호를 위한 조처를 하지 않았다고 주장하고 있다. 사건 당시 이들은 10대였던 것으로 알려졌다."]
    # 원본 데이터 읽기
    # source_df = spark.createDataFrame([(d,) for d in data], ["content"])

    source_df = read_from_postgres(spark)

    # 변환 udf 등록
    udfs = register_udfs()

    # 데이터 처리
    processed_df = process_data(source_df, udfs)
    # print("여기", processed_df)
    # 처리된 데이터 저장
    write_to_postgres(processed_df)
    # print("끝")


if __name__== '__main__':
    main()
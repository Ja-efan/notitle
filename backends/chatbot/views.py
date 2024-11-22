from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler

import time 
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from dotenv import load_dotenv
from django.conf import settings 
from news.models import News # News 모델 import 

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

@csrf_exempt
@api_view(['POST'])
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 파라미터 처리 (기사 id 와 사용자 질문)
            user_input = data.get('question', '')
            article_id = data.get('article_id', '')
            # print(f"기사 ID: {article_id}")
            # print(f"사용자 질문: {user_input}")
            # Postgres DB에서 기사 데이터 가져오기 
            try: 
                article = News.objects.get(article_id = article_id)
                article_title = article.title
                article_content = article.content
                # print(f"사용자 선택 기사 제목: {article_title}")
                # print(f"사용자 선택 기사 내용: \n{article_content}")
            except News.DoesNotExist: 
                print(f"Article({article_id}) Not Found!!!")
                return JsonResponse({"error": f"Article({article_id}) Not Found!!!"}, status=status.HTTP_404_NOT_FOUND)

            # system prompt
            system_prompt = """당신은 사용자의 질문에 대해 친절하고 전문적으로 답변하는 AI 어시스턴트입니다.
            제공된 뉴스 기사를 바탕으로 답변을 생성하되, 기사 내용을 벗어나지 않도록 주의하세요.
            답변은 한국어로 작성하며, 전문적이면서도 이해하기 쉽게 설명해주세요."""            
            # print(system_prompt)

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(
                    content=f"다음 기사를 바탕으로 질문에 답변해주세요.\n\n \
                        기사 제목: {article_title}\n \
                        기사 내용: {article_content}\n\n \
                        질문: {user_input}"
                )
            ]

            response = llm(messages)
            answer = response.content 
            print("OpenAI API 응답 완료 !")
            print(f"GPT 답변: {answer}")

            # 결과 반환
            return JsonResponse({"answer": answer}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

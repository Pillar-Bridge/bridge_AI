#!/usr/bin/env python
# coding: utf-8
import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyCKv73cpWOu7mWuvgoMVm3xp__9b4TpzIE')
model = genai.GenerativeModel('gemini-pro')

#########################################################

chat_session = model.start_chat(history=[]) #ChatSession 객체 반환
# user_queries = ["다음 메시지부터 특정 장소에서 특정 질문에 대한 화자의 답변을 출력하도록 해주세요.", "특정장소(카페)에서 특정 질문(손님 주문하시겠어요?라는 질문에 대한 답변을 해주세요."]
user_queries = ["특정장소(카페)에서 특정 질문(손님 주문하시겠어요?)라는 질문에 대한 답변하기 위한 멘트를 나열 해주세요.", "추가로 카페에서 잘나가는 메뉴를 추천받기 위해 사용하는 멘트를 나열해주세요"]

for user_query in user_queries:
    print(f"[User]: {user_query}")
    response = chat_session.send_message(user_query)
    # 색깔을 입히기 위한 코드
    print(f"[Gemini]: {response.text}")
    

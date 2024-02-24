#!/usr/bin/env python
# coding: utf-8
import google.generativeai as genai
import os
import json 
import datetime

nowadays = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
genai.configure(api_key='AIzaSyCKv73cpWOu7mWuvgoMVm3xp__9b4TpzIE')

generation_config = genai.GenerationConfig(
    candidate_count=1,
    top_k = 5,
    top_p = 0.1, # 0~1 사이의 값으로, 0에 가까울수록 고정적 답변, 1에 가까울수록 창의적인 답변
    temperature= 0 # 0~1 사이의 값으로, 0에 가까울수록 고정적 답변, 1에 가까울수록 창의적인 답변
    # stop_sequences = [". ", "! "] #stop_sequnece에 있는 문자열을 만나면 생성을 중단시킴 
)

model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

query = "특정장소(카페)에서 점원이 특정 질문(손님 주문하시겠어요?)라는 질문에 대한 손님이 주문하기 위한 멘트를 나열 해주세요. 이때 멘트는 5개 안으로 제한해주시고, 총 2가지 상황(주문, 용무)에 대한 멘트를 나열해주세요. 마지막으로 json 파일 형식으로 만들어주세요" 

tokens = model.count_tokens(query) # Token 수 측정

response = model.generate_content(query)

print(f"canidate 생성 건수: {len(response.candidates)}")
print(f"Token 수 : {tokens}") #Eng : 1토큰 = 4글자, Kor : 1토큰 = 1.5글자
print(f"[User] : {query}")
print(f"[AI] : {response.text}")



input_str = response.text

# 첫 번째 '{'와 마지막 '}'의 인덱스를 찾습니다.
start_index = input_str.find('{')
end_index = input_str.rfind('}')

# 첫 번째 '{'부터 마지막 '}'까지의 부분 문자열을 추출합니다.
extracted_json_string = input_str[start_index:end_index+1]
# json 형식으로 저장  
json_data = json.loads(extracted_json_string)

with open(f"./result/{nowadays}.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
result = json.load(open(f"./result/{nowadays}.json", "r", encoding="utf-8"))
# result['주문']
print(result)
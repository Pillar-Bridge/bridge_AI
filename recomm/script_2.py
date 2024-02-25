#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import datetime
import time 
import os

import google.generativeai as genai

api_key = os.getenv('api_key')

def arg_parser():
    # ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description="Generate responses based on place, question, and situations")

    # 각 인자를 추가합니다.
    parser.add_argument("--place", type=str, required=True, help="장소 (문자열)")
    parser.add_argument("--question", type=str, required=True, help="질문 (문자열)")
    parser.add_argument("--situations", nargs="+", required=True, help="상황들 (최소 하나 이상, 문자열로 구성된 리스트)")
    parser.add_argument("--language", type=str, required=True, help="언어 (문자열)")

    # 파싱된 인자들을 받아옵니다.
    args = parser.parse_args()
    return args 

def inverted_lang(language):
    if language == 'ko':
        return '한국어'
    else:
        return 'english' #default : 한국어도 지원가능 
    
def generate_responses(place, question, lang):
    # Google AI 모델 설정
    genai.configure(api_key=api_key)

    # Generation Config 설정
    generation_config = genai.GenerationConfig(
        candidate_count=1,
        top_k=5,
        top_p=0,  # 0~1 사이의 값으로, 0에 가까울수록 고정적 답변, 1에 가까울수록 창의적인 답변
        temperature=0  # 0~1 사이의 값으로, 0에 가까울수록 고정적 답변, 1에 가까울수록 창의적인 답변
        # stop_sequences = [". ", "! "] #stop_sequnece에 있는 문자열을 만나면 생성을 중단시킴
    )

    # GenerativeModel 객체 생성
    model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
    
    # 응답 생성 쿼리 문자열 생성
    # user_queries = [
    #     {
    #         ""
    #     }
    #     {
    #         "role":"user",
    #         "parts": [
    #             f"특정장소({place})에서 상대방이 특정 질문({question})라는 질문에 대해 어떤 상황인지 1줄로 (key : situation)설명하고, 이 상황에서 상대방의 질문에 대응할 수 있는 답변(key : response)을 5개 생성해주세요. 더불어 답변에 대한 비슷한 종류 문장(key : similar)과 반의어 문장(key : antonym), 고유 명사들 대신 사용할 수 있는 후보 명사들(key : nouns, value : [후보 명사 리스트])도 각 답변 문장마다 생성해주세요. 최종적으로 만든 결과물을 {lang}로 만들어주시고,json 형식의 파일로 저장해주세요."
    #         ]
    #     }
    # ]
    # text파일 불러오기 
    # GenerativeModel 객체 생성
    prompt_f = open('/home/bmegpu02/dh/gdsc/recomm/prompt.txt', 'r', encoding='utf-8')
    prompt = prompt_f.read()
    prompt_f_2 = open('/home/bmegpu02/dh/gdsc/recomm/prompt_2.txt', 'r', encoding='utf-8')
    prompt_2 = prompt_f_2.read()
    
    prompt_parts = [
    f"input: 특정장소(cafe)에서 상대방이 특정 질문(Would you like to order?)라는 질문에 대해 어떤 상황인지 명사로 (key : situation)설명하고, 이 상황에서 상대방의 질문에 대응할 수 있는 답변(key : response)을 5개 생성해주세요. 이때, response에 고유명사 부분에 대괄호([])없이 만들어주세요. 더불어 답변에 대한 고유 명사들(대괄호) 대신 사용할 수 있는 후보 명사들(key : nouns, value : [후보 명사 리스트])도 각 답변 문장마다 생성해주세요. 최종적으로 만든 결과물을 (eng)로 만들어주시고,json 형식의 파일로 저장해주세요.",
    f"output: {prompt}",
    f"input: 특정장소(restraunt)에서 상대방이 특정 질문(May I take your order)라는 질문에 대해 어떤 상황인지 명사로 (key : situation)설명하고, 이 상황에서 상대방의 질문에 대응할 수 있는 답변(key : response)을 5개 생성해주세요. 이때, response에 고유명사 부분에 대괄호([])없이 만들어주세요. 더불어 답변에 대한 고유 명사들(대괄호) 대신 사용할 수 있는 후보 명사들(key : nouns, value : [후보 명사 리스트])도 각 답변 문장마다 생성해주세요. 최종적으로 만든 결과물을 (eng)로 만들어주시고,json 형식의 파일로 저장해주세요.",
    f"output: {prompt_2}",
    f"input: 특정장소({place})에서 상대방이 특정 질문({question})라는 질문에 대해 어떤 상황인지 5글자로 명사로 (key : situation)설명하고, 이 상황에서 상대방의 질문에 대응할 수 있는 답변(key : response)을 5개 생성해주면서 response에 고유명사 부분에 대괄호([])없이 만들어주세요. 더불어 답변에 대한 고유 명사들(대괄호) 대신 사용할 수 있는 후보 명사들(key : nouns, value : [후보 명사 리스트])도 각 답변 문장마다 생성해주세요. 최종적으로 만든 결과물을 {lang}로 만들어주시고,json 형식의 파일로 저장해주세요.",
    "output: "
    ]
    response = model.generate_content(prompt_parts)
    # print(response.text)
    save_response_as_json(place, question, response.text, lang) # JSON 파일로 응답 저장
    
    # Google AI 모델을 사용하여 응답 생성
    # history = [] 
    # for query in user_queries:
    #     history.append(query)
    #     response = model.generate_content(history)
    #     history.append(response.candidates[0].content)
        
    #     # print(f"[User] : {query['parts'][0]}")
    #     print(f"[AI] : {response.text}")
    #     # JSON 파일로 응답 저장
    #     save_response_as_json(place, question, response.text, lang)

def check_json(place, question, lang, json_str):
    input_str = json_str
    
    # json 파일형식인경우
    if "```json" in input_str:
        # 첫 번째 '{'와 마지막 '}'의 인덱스를 찾습니다.
        start_index = input_str.find('{')
        end_index = input_str.rfind('}')

        # 첫 번째 '{'부터 마지막 '}'까지의 부분 문자열을 추출합니다.
        extracted_json_string = input_str[start_index:end_index+1]
        # extracted_json을 json 객체로 전환
        extracted_json_string = json.loads(extracted_json_string)
                
        return extracted_json_string, True
    else: #아닌경우 
        generate_responses(place, question, lang)
        return input_str, False
        
def save_response_as_json(place, question, response, lang):
    # 현재 시간을 사용하여 파일명 생성
    # nowadays = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    response, json_tag = check_json(place, question, lang, response)

    # JSON 형식으로 저장할 데이터 생성
    if json_tag:
        # json 형식으로 저장  
        # json_data = json.loads(response)
        with open(f"/home/bmegpu02/dh/gdsc/recomm/result/output.json", "w", encoding="utf-8") as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
        print(f"JSON 파일로 저장되었습니다.")
    else:
        generate_responses(place, question, lang) #원하는 형식이 아니면 다시 실행  


def json_input():
    # JSON 파일을 읽어옵니다.
    with open('/home/bmegpu02/dh/gdsc/recomm/input/testInput.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['place'], data['text'], inverted_lang(data['lang'])

def main():
    # args = arg_parser()
    # 받아온 인자들을 활용하여 응답을 생성합니다.
    start_time = time.time()
    place, question, lang = json_input()
    generate_responses(place, question, lang) #<-- 실행부분
    end_time = time.time()
    print(f"실행시간: {end_time - start_time}")
    
if __name__ == "__main__":
    main()

#python script.py --place "카페" --question "손님 주문하시겠어요?" --situations "주문" "용무"


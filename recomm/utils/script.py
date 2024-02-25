#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import datetime
import os
import google.generativeai as genai

api_key = os.getenv('api_key')

def main():
    # ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description="Generate responses based on place, question, and situations")

    # 각 인자를 추가합니다.
    parser.add_argument("--place", type=str, required=True, help="장소 (문자열)")
    parser.add_argument("--question", type=str, required=True, help="질문 (문자열)")
    parser.add_argument("--situations", nargs="+", required=True, help="상황들 (최소 하나 이상, 문자열로 구성된 리스트)")


    # 파싱된 인자들을 받아옵니다.
    args = parser.parse_args()

    # 받아온 인자들을 활용하여 응답을 생성합니다.
    generate_responses(args.place, args.question, args.situations)


def generate_responses(place, question, situations):
    # Google AI 모델 설정
    genai.configure(api_key=api_key)

    # Generation Config 설정
    generation_config = genai.GenerationConfig(
        candidate_count=1,
        top_k=5,
        top_p=0.1,  # 0~1 사이의 값으로, 0에 가까울수록 고정적 답변, 1에 가까울수록 창의적인 답변
        temperature=0  # 0~1 사이의 값으로, 0에 가까울수록 고정적 답변, 1에 가까울수록 창의적인 답변
        # stop_sequences = [". ", "! "] #stop_sequnece에 있는 문자열을 만나면 생성을 중단시킴
    )

    # GenerativeModel 객체 생성
    model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)

    # 응답 생성 쿼리 문자열 생성
    query = f"특정장소({place})에서 점원이 특정 질문({question})라는 질문에 대한 손님이 대답하기 위한 멘트를 나열 해주세요. 이때 멘트는 5개 안으로 제한해주시고, 각 상황({situations})에 대한 멘트를 나열해주세요. 마지막으로 json 파일 형식으로 만들어주세요"

    # Google AI 모델을 사용하여 응답 생성
    response = model.generate_content(query)

    # 생성된 응답 출력
    print("[AI Response]:", response.text)

    # JSON 파일로 응답 저장
    save_response_as_json(place, question, response.text)
    
    return save_response_as_json(place, question, response.text)
    


def save_response_as_json(place, question, response_text):
    # 현재 시간을 사용하여 파일명 생성
    nowadays = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # JSON 형식으로 저장할 데이터 생성
    json_data = {
        "place": place,
        "question": question,
        "response": response_text
    }

    # JSON 파일로 저장
    with open(f"./result/{nowadays}.json", "w", encoding="utf-8") as f:
    # with open(f"./result/response.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)




if __name__ == "__main__":
    main()


#python script.py --place "카페" --question "손님 주문하시겠어요?" --situations "주문" "용무"
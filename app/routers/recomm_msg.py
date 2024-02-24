from fastapi import APIRouter
import os
import sys
from typing import List
from pydantic import BaseModel
import json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import recomm.run
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/recomm",
    tags=["recomm"],
    responses={404: {"description": "Not found"}},
)

class RequestModel(BaseModel): 
    place: str
    text: str
    lang: str
    
def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_result_json_with_date(data, directory):
    unique_id = uuid.uuid4() 
    file_name = f"{unique_id}.json" 
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    return file_path

@router.post("") 
async def generate_recommendation(request_body: RequestModel):
    request_data = request_body.dict()

    input_file_path = "/home/bmegpu02/dh/gdsc/recomm/input/testInput.json"
    save_json(request_data, input_file_path)

    recommender = recomm.run.get_recommendation()
    recommender.run()

    with open('/home/bmegpu02/dh/gdsc/recomm/result/output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    result_file_path = save_result_json_with_date(data, "/home/bmegpu02/dh/gdsc/recomm/result")

    transformed_json = {
        "situation": data["situation"],
        "response": [item["response"] for item in data["response"]]
    }

    return transformed_json
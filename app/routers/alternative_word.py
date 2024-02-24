from fastapi import APIRouter, HTTPException
import os, sys, json
from typing import List
from pydantic import BaseModel

router = APIRouter(
    prefix="/alter",
    tags=["alter"],
    responses={404: {"description": "Not found"}},
)

class SentenceRequest(BaseModel):
    sentence: str

def clean_up_files(directory):
    files = os.listdir(directory)
    full_paths = [os.path.join(directory, file) for file in files]

    if len(full_paths) > 10:
        sorted_files = sorted(full_paths, key=os.path.getctime)
        for file in sorted_files[:-10]:
            os.remove(file)

@router.post("")
async def get_response_nouns(request: SentenceRequest):
    directory = "/home/bmegpu02/dh/gdsc/recomm/result"
    files = os.listdir(directory)
    full_paths = [os.path.join(directory, file) for file in files]
    sorted_files = sorted(full_paths, key=os.path.getctime, reverse=True)

    for index, file_path in enumerate(sorted_files):
        if index >= 3:
            break

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data['response']:
            if request.sentence == item['response']:
                processed_nouns = [{"word": word, "options": options} for word, options in item['nouns'].items()]
                clean_up_files(directory)
                return processed_nouns

    raise HTTPException(status_code=404, detail="Sentence not found in the files")

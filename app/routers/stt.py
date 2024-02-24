from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from stt.whisper import run_whisper_command


router = APIRouter(
    prefix="/stt",
    tags=["stt"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def speech_to_text(file: UploadFile = File(...)):
    input_file_path = f"/home/bmegpu02/dh/gdsc/stt/data/{file.filename}"

    with open(input_file_path, "wb") as buffer:
        data = await file.read()
        buffer.write(data) 

    output_dir = "../stt/res"
    os.makedirs(output_dir, exist_ok=True)

    run_whisper_command(input_file=input_file_path, output_dir=output_dir)
    output_file_path = f"{output_dir}/{file.filename.split('.')[0]}.txt"

    if not os.path.exists(output_file_path):
        raise HTTPException(status_code=404, detail="text 파일이 생성되지 않았습니다.")
    return FileResponse(output_file_path)
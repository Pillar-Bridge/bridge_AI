from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from pathlib import Path
import json
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tts.run import TextToSpeech

router = APIRouter(
    prefix="/tts",
    tags=["tts"],
    responses={404: {"description": "Not found"}},
)

class TTSRequest(BaseModel):
    text: str
    lang: str
    type: str

def cleanup_files(directory: Path, max_files: int = 3):
    files = list(directory.glob('*'))
    if len(files) > max_files:
        files.sort(key=lambda x: x.stat().st_mtime) 
        for file in files[:-max_files]:
            file.unlink()

def generate_filename(res_dir: Path, extension: str = ".mp3"):
    now = datetime.now().strftime("%Y%m%d")
    existing_files = list(res_dir.glob(f'{now}_*{extension}'))
    next_index = len(existing_files) + 1
    return f"{now}_{next_index:03}{extension}"

@router.post("")
async def text_to_speech(request: TTSRequest):
    data_dir = Path("/home/bmegpu02/dh/gdsc/tts/input")
    res_dir = Path("/home/bmegpu02/dh/gdsc/tts/result")

    cleanup_files(data_dir)
    cleanup_files(res_dir)
    
    tts_filename = generate_filename(res_dir)
    tts_filepath = res_dir / tts_filename

    text_file_path = data_dir / tts_filename.replace(".mp3", ".json")
    with text_file_path.open("w") as f:
        json.dump(request.dict(), f, ensure_ascii=False, indent=4)

    try:
        tts = TextToSpeech()
        tts.run()
        headers = {"Content-Disposition": f"attachment; filename={tts_filename}"}
        return FileResponse(tts_filepath, media_type='audio/mpeg', filename=tts_filename, headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
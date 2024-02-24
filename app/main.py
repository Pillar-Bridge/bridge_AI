from fastapi import FastAPI
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.routers import recomm_msg, tts, alternative_word

app = FastAPI()

app.include_router(recomm_msg.router)
app.include_router(alternative_word.router)
app.include_router(tts.router)

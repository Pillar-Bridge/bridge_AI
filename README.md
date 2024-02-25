# Bridge AI

- Implementation of Bridge's key features using<br>
  - <b>Google Gemini Pro<br>
  - Google Cloud Natural Language<br>
  - Google Cloud TTS</b><br>
  - LLM model of <b>Google AI studio</b>
- Build with <b>FastAPI</b>

<br> 

## How to Install and Run

need:
```
python 3.8x
```

install:
```
git clone https://github.com/Pillar-Bridge/bridge_AI
cd bridge_AI
python -m venv [venv]
[venv]\Scripts\activate
pip install -r requirements.txt
```
run:
```
cd app
uvicorn main:app --reload --host=0.0.0.0 --port=5000
```

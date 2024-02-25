# Bridge AI

- Implementation of Bridge's key features using<br>
  - <b>Google Gemini Pro<br>
  - Google Cloud Natural Language<br>
  - Google Cloud TTS</b><br>
  - LLM model of <b>Google AI studio</b>
- Build with <b>FastAPI</b>

<br>

## Service Description

- DL Flow : Input(Question Audio Data) → Output(Recommendation Audio Data from Gemini pro)

### Question for Other Person
![f3](https://github.com/Pillar-Bridge/bridge_AI/assets/54443308/d08e0c8f-3539-4e1b-99e7-0faadbe6fc78)


### Answering from Gemini with NLP
![f5](https://github.com/Pillar-Bridge/bridge_AI/assets/54443308/3516b05a-fc32-4f80-89c0-b38c1c1b631d)



<br> 

## How to Install and Run

need:
```
python 3.8x (at least)
```

install:
```
git clone https://github.com/Pillar-Bridge/bridge_AI
cd bridge_AI
python -m venv (venv)
(venv)\Scripts\activate
pip install -r requirements.txt
```
run:
```
cd app
uvicorn main:app --reload --host=0.0.0.0 --port=5000
```

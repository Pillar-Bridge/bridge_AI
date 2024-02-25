# Bridge AI

- Implementation of Bridge's key features using<br>
  - <b>Google Gemini Pro<br>
  - Google Cloud Natural Language<br>
  - Google Cloud TTS</b><br>
  - LLM model of <b>Google AI studio</b>
- Build with <b>FastAPI</b>

<br>
## Service Description

DL Flow : Input(Question Audio Data) → Output(Recommendation Audio Data from Gemini pro)

### Question for Other Person
![그림1](https://github.com/Pillar-Bridge/bridge_AI/assets/54443308/b5b29ee4-f2cc-4421-b1b0-a65a19e05230)

### Answering from Gemini with NLP
![그림2](https://github.com/Pillar-Bridge/bridge_AI/assets/54443308/aab54059-4621-4154-be31-c9901f00cf3a)


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

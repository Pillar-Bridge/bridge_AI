#! /usr/bin/env python3
from google.cloud import texttospeech
import os
import pandas as pd
import time 
import json 
"""

# Input : ./input/testInput.json 
# Output : ./result/testInput.mp3

TextToSpeech(text, lang)
text : 변환할 텍스트
lang : 언어 (ko, en)

return : None
"""
class TextToSpeech:
    def __init__(self, text = "Not Response", input_dir = '/home/bmegpu02/dh/gdsc/tts/input', save_dir='/home/bmegpu02/dh/gdsc/tts/result'):
        self.text = text 
        self.input_dir= input_dir
        self.save_dir = save_dir
        self.lang = "en-US"  # 기본값 설정
        self.type = "en-US-Standard-A"  # 기본값 설정
        
    def find_latest_file(self):
        files = os.listdir(self.input_dir)
        files = [f for f in files if f.endswith('.json')]
        if len(files) == 0:
            print("\033[1;32;40m File Unload \033[0m")
        else:
            files = sorted(files, reverse=True)
            if len(files) == 0:
                return None
            
            json_file_path = os.path.join(self.input_dir, files[0])
            with open(json_file_path, 'r') as f:
                data = json.load(f)
                self.text = data['text']
                self.lang = data['lang']
                self.type = data['type']
            self.input_path = json_file_path
            self.save_path = json_file_path.replace('json','mp3').replace(self.input_dir, self.save_dir)
            
    def type_converter(self):
        data = {
            'language_code': ['en-US', 'en-US', 'en-US', 'en-US', 'en-US', 'en-US', 'ko-KR', 'ko-KR', 'ko-KR', 'ko-KR', 'ko-KR', 'ko-KR'],
            'name': ['en-US-Standard-A', 'en-US-Casual-K', 'en-US-Wavenet-A', 'en-US-Wavenet-H', 'en-US-Standard-E', 'en-US-Neural2-H', 'ko-KR-Wavenet-C', 'ko-KR-Standard-C', 'ko-KR-Wavenet-D', 'ko-KR-Standard-D', 'ko-KR-Wavenet-B', 'ko-KR-Wavenet-A'],
            'ssml_gender': ['MALE', 'MALE', 'MALE', 'FEMALE', 'FEMALE', 'FEMALE', 'MALE', 'MALE', 'MALE', 'FEMALE', 'FEMALE', 'FEMALE']
        }

        df = pd.DataFrame(data)
        if self.lang not in df['language_code'].values:
            self.lang = 'en-US' # 기본값 영어로 
            self.type = 'en-US-Standard-A' # 기본 음성 출력
            self.gender = texttospeech.SsmlVoiceGender.MALE
                    
        elif self.lang in df['language_code'].values and self.type not in df['name'].values: # 언어는 존재하지만 type이 안 맞는 경우
            self.type = df[df['language_code'] == self.lang].iloc[0, 1] # 첫번째 것으로 채택
            self.gender = texttospeech.SsmlVoiceGender.MALE 
        else: # 모두 맞는 경우 gender searching searching 
            gender = df[(df['language_code'] == self.lang) & (df['name'] == self.type)].iloc[0, 1]
            if gender == 'MALE':
                self.gender = texttospeech.SsmlVoiceGender.MALE
            else:
                self.gender = texttospeech.SsmlVoiceGender.FEMALE
        print(f"Converted(O/X) Lang Type : {self.lang} {self.type}")
        
    def convert_to_speech(self):
        self.client = texttospeech.TextToSpeechClient()
        self.synthesis_input = texttospeech.SynthesisInput(text = str(self.text))
        
        self.type_converter() #type converter 
        
        self.voice = texttospeech.VoiceSelectionParams(
            language_code = self.lang,
            name = self.type,
            ssml_gender=self.gender
        )
        
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        self.response = self.client.synthesize_speech(
            input = self.synthesis_input,
            voice = self.voice,
            audio_config = self.audio_config
        )
    
        #Save Audio
        with open(self.save_path, "wb") as out:
            out.write(self.response.audio_content)
            print("\033[1;32;40m음성변환 완료\033[0m")
            print(f"\033[1;32;40m입력경로 : {self.input_path}\033[0m")
            print(f"\033[1;32;40m출력경로 : {self.save_path}\033[0m")
    
    def run(self):
        start_time = time.time()
        self.find_latest_file()
        self.convert_to_speech()
        end_time = time.time()
        print(f"\033[1;32;40m실행시간: {end_time - start_time}[Second] \033[0m")
        

if __name__ == "__main__":
    tts = TextToSpeech()
    tts.run()

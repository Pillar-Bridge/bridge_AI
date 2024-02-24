#! /usr/bin/env python3
import os
from gtts import gTTS 
import uuid
import json 
"""
# 1. Text를 입력받는다. : 인자 두개 
# 1-1. 한국어 버전, 영어버전으로 바꾼다. 
# 2. Text를 음성으로 변환한다.
# 3. 음성을 재생한다.

TextToSpeech(text, lang)
text : 변환할 텍스트
lang : 언어 (ko, en)

return : None
"""
class TextToSpeech:
    def __init__(self, text = "Not Response", lang = 'eng', input_dir = '/home/bmegpu02/dh/gdsc/tts/input', save_dir='/home/bmegpu02/dh/gdsc/tts/result'):
        self.lang = lang 
        self.text = text 
        self.input_dir= input_dir
        self.save_dir = save_dir
    
    def json_input(self, json_file_path):
        # json 파일 읽어오기
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
        self.text = data['text']
        self.lang = data['lang']
        self.type = data['type']
        
    def find_latest_file(self):
        files = os.listdir(self.input_dir)
        files = [f for f in files if f.endswith('.json')]
        if len(files) == 0:
            print("\033[1;32;40m File Unload \033[0m")
        else:
            files = sorted(files, reverse=True)
            if len(files) == 0:
                return None
            
            self.json_input(os.path.join(self.input_dir, files[0]))
            self.file_path = os.path.join(self.input_dir, files[0])

    def convert_to_speech(self):
        # 음성으로 변환한다.
        tts = gTTS(text=self.text, lang=self.lang, lang_check=True)
        tts.save(os.path.join(self.save_dir, self.file_path.split('/')[-1].split('.')[0] + '.mp3'))
        
        # 터미널창에서 색깔이 있게 만들어준다.
        print("\033[1;32;40m음성변환 완료\033[0m")
        
    def delete_file(self):
        os.remove("hello.mp3")

    def run(self):
        self.find_latest_file()
        self.convert_to_speech()

if __name__ == "__main__":
    tts = TextToSpeech()
    tts.run()
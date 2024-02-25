#!/usr/bin/env python
# coding: utf-8
import google.generativeai as genai
import os

api_key = os.getenv('api_key')

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("카페에서 커피를 마시고 싶을 때 사용하는 멘트는?")
print(response.text)
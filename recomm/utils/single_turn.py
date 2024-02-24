#!/usr/bin/env python
# coding: utf-8
import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyCKv73cpWOu7mWuvgoMVm3xp__9b4TpzIE')
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("카페에서 커피를 마시고 싶을 때 사용하는 멘트는?")
print(response.text)
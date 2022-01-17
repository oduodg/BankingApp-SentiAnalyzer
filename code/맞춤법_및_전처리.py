# -*- coding: utf-8 -*-
"""맞춤법 및 전처리.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OefR97l55kMcmDfhgQXnB-XjkYLFWmQp
"""

!pip install git+https://github.com/ssut/py-hanspell.git
!pip install tqdm

from google.colab import drive
drive.mount('/content/drive')

# 필요한 패키지 및 함수 import
import io # io없이 pandas만 import할 경우 오류 발생
import pandas as pd
import csv
import re
from hanspell import spell_checker
from tqdm import tqdm

#pd.read_csv로 csv파일 불러오기

kb = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/KB국민은행/raw/KB국민.csv')
nh = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/NH농협은행/raw/NH농협.csv')
sc = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/SC제일은행/raw/sc제일.csv')
sh = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/Sh수협은행/raw/Sh수협.csv')
sinhan = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/신한은행/raw/신한.csv')
woori = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/우리은행/raw/우리.csv')
kakao = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/카카오뱅크/raw/카카오뱅크.csv')
k = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/케이뱅크/raw/케이뱅크.csv')
toss = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/토스뱅크/raw/토스뱅크.csv')
hana = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/하나은행/raw/하나.csv')
city = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/한국씨티은행/raw/씨티.csv')

# ***** bank 설정 *****
bank = kakao
bank_name = 'kakao'

# 'date' 열 형식을 datetime으로 변환
bank['date'] = pd.to_datetime(bank['date'],format='%Y-%m-%d')

# 연도 설정 및 데이터 추출
target_year = 2021
data_2021 = bank.query('date.dt.year == @target_year')

print(target_year, "년도에는 총", len(data_2021), "개의 데이터가 있습니다.")

data_2021.head()

# 텍스트 전처리
def cleanText(text):
  specialChar = '[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》❤♥♡ㅏㅑㅓㅑㅗㅛㅜㅠㅢㅡㅣㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅆㅉㅃ]'
  text = ''.join(c for c in text if c not in specialChar)
  only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF"  #BMP characters 이외 (이모지 제거)
                           "]+", flags=re.UNICODE)
  return only_BMP_pattern.sub(r'', text)

# 맞춤법 검사
def spell_check(comments):
  for k in tqdm(range(len(comments))):
    comments[k] = cleanText(comments[k])
    spelled_sent = spell_checker.check(comments[k])
    checked_sent = spelled_sent.checked
    comments[k] = checked_sent
  print("맞춤법 검사 완료")
  
  #return comments.to_csv(bank_name+'_spell_checked.csv')


spell_check(data_2021['comment'])
data_2021.to_csv(bank_name+"_spell_checked.csv")
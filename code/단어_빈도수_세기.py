# -*- coding: utf-8 -*-
"""단어 빈도수 세기.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JlQ7dBt1d5uXZbi274BqjQpfR0elTZE7
"""

!pip install konlpy

from google.colab import drive
drive.mount('/content/drive')

import io
import pandas as pd
import csv
from konlpy.tag import Komoran
from collections import defaultdict

#pd.read_csv로 csv파일 불러오기

kb = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/kb_spell_checked.csv')
#nh = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/nh_spell_checked.csv')
#sc = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/sc_spell_checked.csv')
#sh = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/sh_spell_checked.csv')
#sinhan = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/sinhan_spell_checked.csv')
#woori = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/woori_spell_checked.csv')
#kakao = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/kakao_spell_checked.csv')
#k = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/k_spell_checked.csv')
#toss = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/toss_spell_checked.csv')
#hana = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/hana_spell_checked.csv')
#city = pd.read_csv('/content/drive/Shareddrives/언어의미와정보 데이터캡스톤디자인/리뷰 데이터/spell_checked/city_spell_checked.csv')

# ***** bank 설정 *****
bank = kb
bank_name = 'kb'

comments = bank['comment']
comments.tail()

komoran = Komoran(userdic='/content/user_dictionary.txt') # userdic 추가

# 고려하는 품사만 tag로 선택
'''
긍정지정사(VCP), 부정지정사(VCN)
일반명사(NNG), 고유명사(NNP), 동사(VV), 형용사(VA), 부사(MAG)
수사(NR), 감탄사(IC), 어근(XR), 보조 용언(VX)
'''
tag_list = ['VCP','VCN',
            'NNG','NNP','VV','VA','MAG',
            'NR','IC','XR','VX']

# 계산할 tag만 남기고 다른 품사는 제거
def remove_word_by_tag(token,tag_list):
  temp = list()
  for k in range(len(token)):
    if token[k][1] in tag_list:
      temp.append(token[k])
    else:
      continue
  return temp


# 형태소 분석
def morph_analysis(comments):
  morph_token = []
  for comment in comments:
    token = komoran.pos(comment)
    token = remove_word_by_tag(token, tag_list)
    morph_token.append(token)
  return morph_token


# 품사별 단어 빈도수 계산
def word_count(part, tokens): # part는 원하는 품사
  part_list = defaultdict(int)
  for token in tokens:
    for k in range(len(token)):
      if token[k][1] == part: # token의 품사가 지정한 품사이면
        part_list[token[k][0]] += 1
  return part_list

i = 1
for comment in comments:
  token = komoran.pos(comment)
  print(i,'번째:', token)
  i += 1

header_list = ['count','WORD','TAG','reinforcer','score']
df = pd.DataFrame(columns=header_list)

morph_token = morph_analysis(comments)
word_list = []
for tag in tag_list:
  word_list = word_count(tag, morph_token)
  sorted_list = sorted(word_list.items(), key=lambda x: x[1], reverse=True)
  for i in range(len(sorted_list)):
    df = df.append({'count':sorted_list[i][1], 'WORD':sorted_list[i][0],'TAG':tag,'reinforcer':1, 'score':0}, ignore_index=True)
    df = df.sort_values('count', ascending=False)
print(df)

df.to_csv(bank_name+'_score_dic.csv')
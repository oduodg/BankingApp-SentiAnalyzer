from google_play_scraper import *
from datetime import datetime
import pandas as pd

reviews = reviews_all(
    'viva.republica.toss',
    sleep_milliseconds=0, # defaults to 0
    lang='ko', # defaults to 'en'
    country='kr', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
    #filter_score_with=5 # defaults to None(means all score)
)


df = pd.DataFrame(columns=['userName','score','date','thumbsUpCount','comment'])
review_cnt = 1

for review in reviews:

    userName = review['userName']
    score = review['score']
    date = review['at']
    thumbsUpCount = review['thumbsUpCount']
    comment = review['content']

    df = df.append({
        'userName': userName,
        'score': score,
        'date': date,
        'thumbsUpCount': thumbsUpCount,
        'comment': comment
    }, ignore_index=True)

    print(review_cnt, "번째 리뷰 수집 완료")
    review_cnt += 1

# finally save the dataframe into csv file
filename = datetime.now().strftime('/Users/eun/Desktop/홍익대학교/2021 3-2/데이터캡스톤디자인,언어의미와정보 옥창수,박상준/팀플/project/playstore_crawling/result/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv(filename, encoding='utf-8-sig', index=False)
print('Done!')

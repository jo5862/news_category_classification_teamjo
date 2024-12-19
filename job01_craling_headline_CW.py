from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

print('hello')
#뉴스 카테고리
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

df_titles = pd.DataFrame()

for i in range(3, 5):
    # 네이버 뉴스 기사
    url = 'https://news.naver.com/section/10{}'.format(i)
    resp = requests.get(url)
    ## request응답을 html 파일로 정리해 줌
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sa_text_strong')
    titles = []
    for title_tag in title_tags:

        title = title_tag.text

        #데이터 전처리
        #^가-힣 쓸때 공백 한개 필수!!
        #sub('', title) 는 빼고 공백을 넣으라는 의미
        title = re.compile('[^가-힣 ]').sub('', title)
        titles.append(title)

    df_section_titles = pd.DataFrame(titles, columns = ['titles'])
    df_section_titles['category'] = category[i]

    df_titles = pd.concat([df_titles, df_section_titles], axis = 'rows', ignore_index = True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

df_titles.to_csv('./crawling_data/naver_headline_news_CW_{}.csv'.format(
    #strf -> standard format date
    datetime.datetime.now().strftime('%Y%m%d')), index=False)


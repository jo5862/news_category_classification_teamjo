from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

print('hello')
#뉴스 카테고리
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

df_titles = pd.DataFrame()

#세환 for i in range(0,1):
#동준 for i in range(1,3):
#지민 for i in range(3,5):
#재상 for i in range(5,6):

for i in range(1, 3):
    # 네이버 뉴스 기사
    url = 'https://news.naver.com/section/10{}'.format(i)
    resp = requests.get(url)
    # request응답을 html 파일로 정리해 줌
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sa_text_strong')
    titles = []
    for title_tag in title_tags:
        title = title_tag.text

        # 데이터 전처리
        # ^가-힣 쓸때 공백 한개 필수!!
        # sub('', title) 는 빼고 공백을 넣으라는 의미
        title = re.compile('[^가-힣 ]').sub('', title)
        titles.append(title)

    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]

    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

    # Save the file with category name in the filename
    filename = './crawling_data/naver_headline_news_{}_{}.csv'.format(
        datetime.datetime.now().strftime('%Y%m%d'), category[i])
    df_section_titles.to_csv(filename, index=False)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

# df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
#     #strf -> standard format date
#     datetime.datetime.now().strftime('%Y%m%d')), index=False)


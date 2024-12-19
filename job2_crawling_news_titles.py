from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime


options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

options.add_argument('user_agent=' + user_agent)
options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

url ='https://news.naver.com/section/100'
driver.get(url)

#더보기 버튼 Xpath
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]/a'

# 클롤링 한 제목 1차 저장할 리스트
titles = []

# 카테고리와 합쳐서 저장할 데이터 프레임
df_titles = pd.DataFrame()

# 15번 기사 더보기 버튼 클릭
for i in range(15):
    time.sleep(0.5)
    driver.find_element(By.XPATH, button_xpath).click()

# 97개의 div에서
for i in range(1,98):

    # 6개의 기사제목 뽑기
    for j in range(1,7):

        title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i,j)
        try:
            title = driver.find_element(By.XPATH, title_xpath).text
            print(title)

            title = re.compile('[^가-힣 ]').sub('', title)

            #titles 리스트에 title 추가하기
            titles.append(title)

        except:
            print(i, j)


df_titles = pd.DataFrame(titles, columns=['titles'])

#category 컬럼 추가
df_titles['category'] = category[1]

# df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)

# Save the file with category name in the filename
filename = './crawling_data/naver_headline_news_{}_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d'), category[1] )

df_titles.to_csv(filename, index=False)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())

time.sleep(30)
driver.close()


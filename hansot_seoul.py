import urllib
from bs4 import BeautifulSoup
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sys
import time
import pandas as pd


# A. 데이터 크롤링

# 0. 수집 준비
# 1-1) user-agent 준비
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
headers = {'User-Agent':user_agent, 'Referer':None}


# 2. 수집 준비
#https://m.map.naver.com/search2/search.naver
#?query=한솥%20서울시%20강남구
#&sm=hty&style=v5

# 2-1) 필요한 변수를 설정


sido = ["서울특별시", "경기도", "부산광역시"]
seoul = ["강남구", "강동구", "강북구", "강서구", "광진구"]
gyeonggi = ["광명시", "수원시", "평택시", "안양시", "하남시"];
busan = ["강서구", "금정구", "해운대구", "동구", "북구"];

gugun_dict = {"서울특별시":seoul, "경기도":gyeonggi,  "부산광역시":busan}

for a in sido :
    for s in range(5) :
        print(gugun_dict[a][s])
        
        # 1. 브라우저 제어를 위한 객체 생성
        driver = webdriver.Chrome('data/chromedriver.exe')
        driver.implicitly_wait(3)
        
        keyword = '한솥%20' + a + '%20' + gugun_dict[a][s]
        base_url = 'https://m.map.naver.com/search2/search.naver'
        
        # 파라미터를 딕셔너리로 준비
        base_param = 'query=' + keyword 
        sub_param = {'sm':'hty', 'style':'v5'}
        
        # 3. 반복 수행으로 데이터 수집하기
        # 수집 결과를 저장할 빈 리스트
        # => [{매장1}, {매장2}, {매장3}, ...]
        data_list = []
        
        # 1) url 준비
        # URLEncoding => utf-8로 설정 ('한솥+서울시+강남구'를 '%EC%B9%B4%EB%A9%94%EB%9D%BC' 형식으로 전환)
        sub_query = urllib.parse.urlencode(sub_param)
        # url 완성
        content_url = base_url + '?' + base_param + '&' + sub_query
        #print(content_url)
        
        # 2) 상품 정보 수집
        driver.get(content_url)
        time.sleep(10)
        
        # 전체 검색 결과를 감싸고 있는 태그가 있는지 검사
        # -> 검색페이지가 변경되었는지 검사
        try :
            WebDriverWait(driver, 3).until(
                lambda drv : drv.find_element_by_css_selector('.search_list._items'))
        except Exception as e :
            print('네이버 지도 페이지의 소스구성이 변경되어 크롤링 종료 >>', e)
            driver.quit()
            sys.exit()
        
        # 스크롤을 맨아래로 이동
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)
        
        
        
        # 3) BeautifulSoup 객체 생성
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 상품 정보 박스 추출
        info_list = soup.select('li._item._lazyImgContainer')
        info_list_test = info_list
        
        body_list_test = soup.select('.sp_map.btn_spi2.naver-splugin')
        
        #print(body_list_test[:1])
        
        #print(len(info_list_test))
        #print(info_list_test[:1])
        #print('-'*30)
        
        # 4-1) 수집한 태그에서 매장위도 추출(data-latitude)
        latitude_list = []
        
        for title in info_list_test :
            if 'data-latitude' in title.attrs :
                k = 'latitude'
                latitude_list.append(title['data-latitude'])
                
        #print(len(latitude_list))
        #print(latitude_list)
        
        # 4-2) 수집한 태그에서 매장경도 추출(data-longitude)
        longitude_list = []
        
        for title in info_list_test :
            if 'data-longitude' in title.attrs :
                k = 'longitude'
                longitude_list.append(title['data-longitude'])
                
        #print(len(longitude_list))
        
        # 4-3) 매장명, 번호, 주소 추출(data-longitude)
        body_list = []
        
        for title in body_list_test :
            if 'data-mail-body' in title.attrs :
                body_list.append(title['data-line-title'])
                #print(title['data-mail-body'])
        
        #print(len(body_list))
        
        data_dict = {}
        data_list = []
        
        for v in body_list :
            
            tmp = v.split('\n')
            key= []
            value = []
            
            if len(tmp) == 3 :
                key = ['name','phone','adr']
               
                name = tmp[0].strip()
                phone = tmp[1].strip()
                adr = tmp[2].strip()
                
                value.append(name)
                value.append(phone)
                value.append(adr)
                
                data_dict = {k:v for k, v in zip(key, value)}
                
                data_list.append(data_dict)
            elif len(tmp) == 2:
                key = ['name','phone','adr']
               
                name = tmp[0].strip()
                adr = tmp[1].strip()
                phone = '00-000-0000'
                
                value.append(name)
                value.append(phone)
                value.append(adr)
                
                data_dict = {k:v for k, v in zip(key, value)}
                
                data_list.append(data_dict)
        
        #print(data_list)        
        
        df = DataFrame(data_list)
        df['위도'] = latitude_list
        df['경도'] = longitude_list
        df1 = df.rename(columns={'name':'매장명', 'phone':'전화번호', 'adr':'주소'})
        
        #드라이버 종료
        driver.quit()
        
        # B. 데이터 전처리 
        # 강남구 불포함 데이터 삭제
        #print(df1)
        df2 = df1
        
        #print(df1['주소'].str.contains('강남구'))
        # -> False인 행 제거하기
        
        df2['trueOrFalse'] = df1['주소'].str.contains(gugun_dict[a][s])
        #print(df2)
        
        df2 = df2.loc[df2.trueOrFalse != False]
        #print(df2)
        
        df2 = df2.drop(['trueOrFalse'], axis=1)
        #print(df2)
        
        # '한솥도시락'이포함된 곳만 남기기
        df2['trueOrFalse'] = df1['매장명'].str.contains('한솥도시락')
        #print(df2)
        
        df2 = df2.loc[df2.trueOrFalse != False]
        #print(df2)
        
        df2 = df2.drop(['trueOrFalse'], axis=1)
        #print(df2)
        
        df2.to_excel(a + '_' + gugun_dict[a][s] + '.xlsx')
        print('저장완료')


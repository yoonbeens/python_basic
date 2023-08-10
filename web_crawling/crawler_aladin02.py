import time as t
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# 뷰티풀수프 임포트
from bs4 import BeautifulSoup
# 날짜 정보 얻어오는 모듈 (연, 월, 일, 시, 분, 초)
from datetime import datetime
import codecs

d = datetime.today()

file_path = f'C:/test/알라딘 베스트셀로 1~400위_{d.year}_{d.month}_{d.day}.txt'

'''
- with문을 사용하면 with 블록을 벗어나는 순간
객체가 자동으로 해제됩니다. (자바의 try with resource과 비슷)

- with 작성 시 사용할 객체의 이름을 as 뒤에 작성해 줍니다.
'''

'''
* 표준 모듈 codecs

- 웹이나 다른 프로그램의 텍스트 데이터와
파이썬 내부의 텍스트 데이터의 인코딩 방식이 서로 다를 경우에
내장함수 open()이 제대로 인코딩을 적용할 수 없어서
에러가 발생합니다. (UnicodeEncodeError)

- 파일 입/출력 시 인코딩 코덱을 변경하고 싶다면
codecs 모듈을 사용합니다.
'''

with codecs.open(file_path, mode='w', encoding='utf-8') as f:

    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)

    service = webdriver.ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service ,options=options)

    driver.get('https://www.aladin.co.kr')

    t.sleep(2)

    #베스트셀러 탭 클릭
    driver.find_element(By.XPATH, '//*[@id="Wa_header1_headerTop"]/div[2]/div[3]/ul[1]/li[3]/a').click()

    t.sleep(2)

    n = 3

    rank = 1 # 순위

    while n < 11:

        

        # selenium으로 현재 페이지의 html 소스 코드를 전부 불러오기
        src = driver.page_source
        # print(src)

        # 뷰티풀수프 객체 생성
        # 뷰티풀수프 객체를 생성하면서, 셀레니움이 가지고 온 html 소스코드를
        # 제공하고, 해당 소스코드를 html 문법으로 변환하라는 주문.
        soup = BeautifulSoup(src, 'html.parser')

        '''
        - 뷰티풀수프를 사용하여 수집하고 싶은 데이터가 들어있는
        태그를 부분 추출할 수 있습니다.

        - find_all() 메서드는 인수값으로 추출하고자 하는 태그의
        이름을 적으면 해당 태그만 전부 추출하여 리스트에 담아 대입합니다.
        '''

        
        div_list = soup.find_all('div', class_='ss_book_box')
        # print('div_list에 들어 있는 데이터 수:', len(div_list)) -> 50개
        # print(div_list[0]) # 1위 책만 한번 가져와 보자

        

        for div in div_list:

            book_info = div.find_all('li')

            if book_info[0].find('span', class_='ss_ht1') == None:
                # first li span class="ss_ht1" not exist
                book_title = book_info[0].text
                book_author = book_info[1].text
                book_price = book_info[2].text
            else:
                book_title = book_info[1].text
                book_author = book_info[2].text
                book_price = book_info[3].text

            auth_info = book_author.split('|')

            f.write(f'# 순위: {rank}위 \n')
            f.write(f'# 제목: {book_title} \n')
            f.write(f'# 저자: {auth_info[0]} \n')
            f.write(f'# 출판사: {auth_info[1]} \n')
            f.write(f'# 출판일: {auth_info[2]} \n')
            f.write('# 가격:' +  book_price.split(', ')[0] + '\n')
            f.write('-' * 40 + '\n')
            rank += 1

        n +=1
        # 한 페이지의 크롤링이 완료된 후
        if n == 11:
            break
        best_tap = f'//*[@id="newbg_body"]/div[4]/ul/li[{n}]/a'
        driver.find_element(By.XPATH, best_tap).click()

            

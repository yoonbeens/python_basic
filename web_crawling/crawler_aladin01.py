import time as t
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# cmd -> pip install bs4
# 뷰티풀수프 임포트
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

service = webdriver.ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service ,options=options)

driver.get('https://www.aladin.co.kr')

t.sleep(2)

#베스트셀러 탭 클릭
driver.find_element(By.XPATH, '//*[@id="Wa_header1_headerTop"]/div[2]/div[3]/ul[1]/li[3]/a').click()

t.sleep(2)

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

# li 안에 우리가 필요로 하는 텍스트가 존재.
# 2, 3, 4번째 li의 텍스트를 가져와야 하겠더라.
first_book = div_list[1].find_all('li')
# print(first_book)

# text(by뷰티풀숲)는 태그를 제외한 사용자가 실제로 브라우저에서 확인 가능한
# 텍스트만을 추출하여 문자열 형태로 반환합니다.

book_title = first_book[1].text
book_author = first_book[2].text
book_price = first_book[3].text

auth_info = book_author.split('|')

print('# 제목:', book_title)
print('# 저자:', auth_info[0])
print('# 출판사:', auth_info[1])
print('# 출판일:', auth_info[2])
print('# 가격:', book_price.split(', ')[0])


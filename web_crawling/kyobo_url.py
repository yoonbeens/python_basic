from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
# 뷰티풀수프 임포트
from bs4 import BeautifulSoup
# 날짜 정보 얻어오는 모듈 (연, 월, 일, 시, 분, 초)
from datetime import datetime
import codecs


d = datetime.today()

file_path = f'C:/test/교보문고 베스트셀러 1~20위_{d.year}_{d.month}_{d.day}.html'

with codecs.open(file_path, mode='w', encoding='utf-8') as f:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)

    service = webdriver.ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service ,options=options)

    driver.get('https://product.kyobobook.co.kr/bestseller/online?period=001#?page=1&per=20&ymw=&period=001&saleCmdtClstCode=&dsplDvsnCode=000&dsplTrgtDvsnCode=001&saleCmdtDsplDvsnCode=')

    time.sleep(1.5)

    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')

    title_list = soup.find_all('li', class_='prod_item')
    print(len(title_list))

    rank = 1

    f.write('<!DOCTYPE HTML> \r\n')
    f.write('<html> \r\n')
    f.write('<head> \r\n')
    f.write('<meta charset="UTF-8"> \r\n')
    f.write('<title>교보 베스트셀러 1~20위</title> \r\n')
    f.write('</head> \r\n')
    f.write('<body> \r\n')

    for idx in range(len(title_list)):
        f.write('<p> \r\n')
        f.write(f'<b>순위: {rank}위</b> <br> \r\n')
        a_url = str(title_list[idx].find('a', class_='prod_link'))
        # href = a_url.get('href') 태그 요소에서 속성 얻어오기.
        # print(href)
        f.write(a_url + '\n <hr> \n' )
        rank += 1
        f.write('</p> \r\n')




    f.write('</body> \r\n')
    f.write('</html> \r\n')
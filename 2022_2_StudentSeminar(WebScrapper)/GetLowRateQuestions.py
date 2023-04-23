import os
#import urllib.request as ur
#from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from PIL import Image


driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.ebsi.co.kr/ebs/xip/xipa/retrieveSCVMainInfo.ebs?irecord=202209013&targetCd=D300&cookieGradeVal=high3')
driver.implicitly_wait(10)
driver.set_window_size(1280, 700)
searchbox = driver.find_element('xpath','//*[@id="nsMenuType6"]')
searchbox.click() #오답률TOP15

def chooseSubject():
    while(True): #1.국어 2.수학 3.영어 4.한국사 11~19.사탐 21~28.과탐
        subject=int(input("1. 국어\n2. 수학\n3. 영어\n4. 한국사\n5. 사탐\n6. 과탐\n원하는 과목의 번호를 입력하세요: "))
        if(subject==1 or 2 or 3 or 4):
            return subject
            break
        elif(subject==5):
            subject=int(input("1. 생활과 윤리\n2. 윤리와사상\n3. 한국지리\n4. 세계지리\n5. 동아시아사\n6. 세계사\n7. 정치와 법\n8. 경제\n9. 사회문화\n원하는 과목의 번호를 입력하세요: "))
            subject=subject+10
            return subject
            break
        elif(subject==6):
            subject=int(input("1. 물리 I\n2. 물리 II\n3. 화학I\n4. 화학II\n5. 생명I\n6. 생명II\n7. 지구과학I\n8. 지구과학II\n원하는 과목의 번호를 입력하세요: "))
            subject=subject+20
            return subject
            break

def getImage(subject,aq):
    
    #과목 설정 하기
    table = driver.find_element('xpath','//*[@id="grdCutArea"]/div[2]/div[2]/table')
    tbody = table.find_element(By.TAG_NAME,'tbody')
    rows = tbody.find_elements(By.TAG_NAME,'tr')
    for index, value in enumerate(rows):
        body=value.find_elements(By.TAG_NAME,'td')[10]
        body.click()
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(10)
        if aq=='q': 
            aq='문제'
        else: 
            aq='해설'
            searchbox = driver.find_element(By.CLASS_NAME,'btn_wrap')
            searchbox.click() #해설
        driver.set_window_size(990, 2180)
        url=driver.current_url
        print(url)
        sleep(3)
        driver.save_screenshot('./'+aq+'/'+str(subject)+'_'+str(index+1)+aq+'.png')
        driver.switch_to.window(driver.window_handles[0])

def mergePDF(aq):
    if aq=='q': 
        aq='문제'
    else: aq='해설'
    file_list = os.listdir('./'+aq)
    img_list = []
    for i in file_list:
        img = Image.open('./'+aq+"\\"+str(i))
        img_1 = img.convert('RGB')
        img_list.append(img_1)
    img_1.save('./\\'+aq+'.pdf',save_all=True, append_images=img_list)
    print()


subject=chooseSubject()
getImage(subject,'q')
getImage(subject,'a')
mergePDF('q')
mergePDF('a')


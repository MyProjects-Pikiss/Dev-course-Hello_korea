import os
import django
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import time, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hello_Korea.settings")
django.setup()

from GyeongJu.KoreaTradition.models import TraditionExperienceInfo, TypeInfo, LanguageInfo, Tradition_form
from GyeongJu.KoreaTradition.experience_constant import *

languages = ['en', 'ja', 'zh-cn', 'zh-tw', 'de', 'ru']


# DB 저장 함수
def DataSave(names, descriptions, call, address, homepage, typeinfo):
    translator = Translator()
    length = len(names)
    
    language = LanguageInfo(lang = 'ko', selected = True)
    language.save()
    for i in range(length):
        culture_experience = TraditionExperienceInfo(
            lang = language,
            name = names[i],
            info = descriptions[i],
            call = call[i],
            address = address[i],
            homepage = homepage[i],
            type = typeinfo,
        )
        culture_experience.save()
        form_text = Tradition_form(
            lang='ko',
            koreaTradition = '전통문화 체험',
            clothTradition = '옷 착의 체험',
            lodgeTradition = '고택 체험',
            tel_num = '전화번호',
            address_text = '주소',
            homepage_text = '홈페이지 가기',
        )
        form_text.save()

    for lang in languages:
        time.sleep(random.random())
        new_data = Tradition_form(
            lang=lang, 
            koreaTradition = translator.translate(form_text.koreaTradition, src='ko', dest=lang).text,
            clothTradition = translator.translate(form_text.clothTradition, src='ko', dest=lang).text,
            lodgeTradition = translator.translate(form_text.lodgeTradition, src='ko', dest=lang).text,
            tel_num = translator.translate(form_text.tel_num, src='ko', dest=lang).text,
            address_text = translator.translate(form_text.address_text, src='ko', dest=lang).text,
            homepage_text = translator.translate(form_text.homepage_text, src='ko', dest=lang).text,
        )
        new_data.save()

        language = LanguageInfo(lang=lang, selected=False)
        language.save()
        for i in range(length):
            time.sleep(0.1)
            culture_experience = TraditionExperienceInfo(
                lang = language,
                name = translator.translate(names[i], src='ko', dest=lang).text,
                info = translator.translate(descriptions[i], src='ko', dest=lang).text,
                call = call[i],
                address = translator.translate(address[i], src='ko', dest=lang).text,
                homepage = homepage[i],
                type = typeinfo,
            )
            culture_experience.save()

# 전통문화체험에 쓰이는 크롤러
def ListCrawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    typename = soup.find('h3', id='pageTitle').text
    typeinfo = TypeInfo(type=typename) # 타입 설정
    typeinfo.save()

    result = soup.find('div', 'exper2')
    names = result.find_all('dt')
    descriptions = result.find_all('dd')
    additional_info = result.find_all('ul')
    call = []
    address = []
    homepage = []
    # 문화체혐명, 설명 초기화
    for i in range(len(names)):
        names[i] = names[i].text
        descriptions[i] = descriptions[i].text
        
    for info in additional_info:
        item = info.find_all('li')
        # 문의전화의 텍스트 형태가 '문의전화 000-000-0000' 형태 여서 불필요 요소 제거가 필요.
        call.append(item[0].text.replace('문의전화 ', ''))
        address.append(item[1].text.replace('주소 ', ''))
        homepage.append(item[2].text.replace('홈페이지 ', ''))
        
    DataSave(names, descriptions, call, address, homepage, typeinfo)

# 의복체험, 고택체험에 쓰이는 크롤러
def TableCrawler(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    typename = soup.find('h3', id='pageTitle').text
    typeinfo = TypeInfo(type=typename) # 타입 설정
    typeinfo.save()

    names = []
    descriptions = []
    call = []
    address = []
    homepage = []
    table = soup.find_all('table')
    table_row = []
    for i in table:
        tr = i.find('tbody').find_all('tr')
        for j in tr:
            table_row.append(j)
    
    if typename == '의복체험':
        for item in table_row:
            cell = item.find_all('td')
            names.append(cell[0].text)
            address.append(cell[1].text)
            descriptions.append(cell[2].text.replace('</li>', '').replace('ul', '').replace('</ul>', '').replace('<li>', '').strip())
            if len(cell[3].find_all('li')) == 0:
                call.append(cell[3].text)
                homepage.append('')
            else:
                contact = cell[3].find_all('li')
                call.append(contact[0].text)
                homepage.append(contact[1].find('a').attrs['href'])
    else:
        for item in table_row:
            cell = item.find_all('td')
            names.append(cell[0].text)
            descriptions.append(cell[1].text)
            if len(cell[3].find_all('a')) == 0:
                homepage.append('')
            else:
                homepage.append(cell[3].find('a').attrs['href'])
            contact = cell[2].find_all('li')
            call.append(contact[0].text.replace('전화 : ', '').replace('\n', ' ').strip())
            address.append(contact[1].text.replace('주소 : ', '').replace('주소: ', '').strip())
    DataSave(names, descriptions, call, address, homepage, typeinfo)

# 크롤링 실행
if __name__ == '__main__':
    ListCrawler(EXPERIENCE_URL)
    TableCrawler(CLOTHES_URL)
    TableCrawler(TRADITIONAL_ACCOMODATION_URL)
    
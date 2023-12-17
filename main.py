import requests
from bs4 import BeautifulSoup
import json
import time
import re

def get_html_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            return None
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

def extract_info(html_content):
    try:
        soup = BeautifulSoup(html_content, 'lxml')
        benefits_div = soup.find('div', class_='title_banner_product_benefits-163')
        name_div = soup.find('div', class_='title_banner_product__info-83e')
        advantages_elements = soup.find_all('div', class_='advantages_item_item-dc2')
        #print(advantages_elements)
        advantages_list = []
        result = {'conditions': ''}
        for element in advantages_elements:
            #print(element)
            advantage_text = re.sub(r'\s+', ' ', element.find('h5', class_='typography-9e2').text.strip())
            advantage_desc = re.sub(r'\s+', ' ', element.find('div', class_='advantages_item_item__desc-dc2').text.strip())
            #print(advantage_text, advantage_desc)
            advantages_list.append({'text': advantage_text, 'desc': advantage_desc})

        if benefits_div and name_div:
            benefit_items = benefits_div.find_all('div', class_='title_banner_product_benefit-a20')
            name = name_div.find('h1').text.strip()


            for item in benefit_items:
                text = re.sub(r'\s+', ' ', item.find('span', class_='title_banner_product_benefit__title-a20').text.strip())
                title = re.sub(r'\s+', ' ', item.find('p', class_='title_banner_product_benefit__text-a20').text.capitalize())
                result['conditions'] += title + ' ' + text + '. '

            result['advantages'] = advantages_list
            return result
        else:
            print("Не удалось найти элемент с классом 'title_banner_product_benefits-163'")
            benefit_elements = soup.find_all('div', class_='title_banner_benefits_benefit-a53')

            for element in benefit_elements:
                text = re.sub(r'\s+', ' ', element.find('div', class_='title_banner_benefits_benefit__title-a53').text.strip())
                title = re.sub(r'\s+', ' ', element.find('div', class_='title_banner_benefits_benefit__text-a53').text.strip().capitalize())
                result['conditions'] += title + ' ' + text + '. '

            result['advantages'] = advantages_list
            return result
    except Exception as e:
        print(f"Произошла ошибка при извлечении информации: {str(e)}")
        return {}

def parse_data(html_code):
    soup = BeautifulSoup(html_code, 'lxml')
    page_data = {}
    divs = soup.find_all('div', class_='product_listing_base_card-30e')
    #print(divs)
    for div in divs:
        link = 'https://www.gazprombank.ru' + div.find('a', class_='product_listing_base_card_description__title-47b')['href']
        div_data = {
            'title': div.find('a', class_='product_listing_base_card_description__title-47b').text.strip(),
            'description': div.find('p', class_='product_listing_base_card_description__subtitle-47b').text.strip(),
            'interest_rate': div.find('span', class_='product_listing_base_card_benefit__title-38c').text.strip(),
            'benefit_description': div.find('div', class_='product_listing_base_card_benefit__desc-38c').text.strip(),
        }
        #time.sleep(0.5)
        div_data.update(extract_info(get_html_content(link)))
        #print(div_data)
        if div_data:
            page_data[div_data['title']] = div_data
        else:
            print("No div_data")

    divs = soup.find_all('div', class_='product_listing_item-647')
    #print(divs)
    for div in divs:
        link = 'https://www.gazprombank.ru' + div.find('a', class_='product_listing_item__title-647')['href']
        ben1 = div.find('h6', class_='typography_h6-9e2')
        ben2 = div.find_all('h6', class_='typography_h6-9e2')[1]
        ben3 = div.find_all('h6', class_='typography_h6-9e2')[2]
        div_data = {
            'title': div.find('a', class_='product_listing_item__title-647').text.strip(),
            'description': div.find('p', class_='typography_css_vars-9e2').text.strip(),
            'benefits': re.sub(r'\s+', ' ', ben1.find_next('p').text.strip().capitalize()) + ' ' + re.sub(r'\s+', ' ', ben1.text.strip()) + '. ' + re.sub(r'\s+', ' ', ben2.find_next('p').text.strip().capitalize()) + ' ' + re.sub(r'\s+', ' ', ben2.text.strip()) + '. ' + re.sub(r'\s+', ' ', ben3.find_next('p').text.strip().capitalize()) + ' ' + re.sub(r'\s+', ' ', ben3.text.strip()) + '.'

        }
        #time.sleep(0.5)
        div_data.update(extract_info(get_html_content(link)))
        if div_data:
            page_data[div_data['title']] = div_data
        else:
            print("No div_data")

    if page_data:
        return page_data
    else:
        print("No page_data")
        return None

urls = ["https://www.gazprombank.ru/personal/take_credit/consumer_credit/", "https://www.gazprombank.ru/personal/credit-cards/?cardIds=6125247,7396061,4594717",
        "https://www.gazprombank.ru/personal/mortgage/", "https://www.gazprombank.ru/personal/avtokredit/", "https://www.gazprombank.ru/personal/increase/deposits/",
        "https://www.gazprombank.ru/personal/accounts/", "https://www.gazprombank.ru/personal/cards/?cardIds=7498685,5880569"]

unavtive_urls = []

all_data = {}

for url in urls:
    html_content = get_html_content(url)

    if html_content:
        result_data = parse_data(html_content)

        if not result_data:
            print("Не удалось получить необходимую информацию.")
        else:
            all_data.update(result_data)

if all_data:
    with open("short_info.json", "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=2)
    print("Информация сохранена в файл credit_info.json")
else:
    print("Не удалось получить необходимую информацию.")
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from decorator import logger


def f_headers():
    headers = Headers(browser='chrome', os='win')
    return headers.generate()


response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=f_headers())

hh_main = response.text
soup = BeautifulSoup(hh_main, features='lxml')
content = soup.find('div', class_="vacancy-serp-content")
vacancys = content.find_all('div', class_="vacancy-serp-item__layout")
# pprint(b)

def job_selection(vacancys):
    list_links = []
    for vacancy in vacancys:
        user_content = vacancy.find('div', class_='g-user-content')
        u_c_text = user_content.text
        if "Flask" in u_c_text and "Django" in u_c_text:
            title = vacancy.find('a')
            href = title['href']
            list_links.append(href)
    return list_links

@logger('test.log')
def pars_vacancy(list_links):
    result = []
    for link in list_links:
        response_link = requests.get(f'{link}', headers=f_headers())
        hh_vacancy = response_link.text
        soup = BeautifulSoup(hh_vacancy, features='lxml')
        vacancy = soup.find('div', class_="bloko-columns-row")
        salary = vacancy.find('span')
        location_company = soup.find('div', class_="vacancy-company-redesigned")
        company = location_company.find('span')
        location = location_company.find('p')
        res = {
            'link': link,
            'salary': salary.text,
            'company': company.text,
            'location': location.text
        }
        result.append(res)
    return result

if __name__ == "__main__":
    list_links = job_selection(vacancys)
    result = pars_vacancy(list_links)
    # print(result)

    with open("vacancy.json", "w", encoding='utf-8') as f:
        json.dump(result, f, indent=5)
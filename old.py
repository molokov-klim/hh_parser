from os import name
import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import datetime
import json
import logging
from config import HH_HEADERS


def get_links(ua, text):
    links = []
    res = requests.get(
        url=f"https://hh.ru/search/vacancy?text={text}&from=suggest_post&fromSearchLine=true&area=1&page=1&hhtmFrom=vacancy_search_list",
        headers={"user-agent": ua.random}
    )
    if res.status_code != 200:
        print("[SYS] Error in get_links(): status code not 200")
        return
    soup = BeautifulSoup(res.content, "lxml")
    try:
        page_count = int(
            soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                "span").text)
        print("page_count: ", page_count)
        for page in range(page_count):
            try:
                res = requests.get(
                    url=f"https://hh.ru/search/vacancy?text={text}&from=suggest_post&fromSearchLine=true&area=1&page={page}&hhtmFrom=vacancy_search_list",
                    headers={"user-agent": ua.random}
                )
                print(res)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.content, "lxml")
                    for a in soup.find_all("a", attrs={
                        "class": "bloko-button bloko-button_kind-primary bloko-button_scale-small"}):
                        # print(f'https://hh.ru{a.attrs["href"]}')
                        links.append(f'https://hh.ru{a.attrs["href"]}')
            except Exception as e:
                logging.error(e)
            print("page: ", page)
            time.sleep(1)
    except Exception as e:
        logging.error(e)
    return links


def list_to_json(list_obj):
    dict_obj = {}
    for i in range(len(list_obj)):
        dict_obj[i] = list_obj[i]
    json_object = json.dumps(dict_obj, indent=4)
    return json_object


def write_list_to_json_file(list_obj, filename):
    json_obj = list_to_json(list_obj)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=4)


def json_file_to_dict(filename):
    f = open(filename)
    data = json.load(f)
    data = json.loads(data)
    f.close()
    return data


def authorized_request():
    session = requests.Session()
    # ПОИСК PYTHON
    link = "https://hh.ru/search/vacancy?text=python&from=suggest_post&fromSearchLine=true&area=1"
    header = HH_HEADERS
    responce = session.get(url=link, headers=header)

    cookies_dict = [
        {'domain': key.domain, 'name': key.name, 'path': key.path, 'value': key.value}
        for key in session.cookies
    ]

    session2 = requests.Session()

    for cookies in cookies_dict:
        session2.cookies.set(**cookies)

    # ОТКЛИКИ И ПРИГЛАШЕНИЯ
    link2 = 'https://hh.ru/applicant/negotiations?hhtmFrom=vacancy_search_list&hhtmFromLabel=header'
    res = session2.get(url=link2, headers=header)

    if res.status_code != 200:
        print("[SYS] Error in get_links(): status code not 200")
        return
    soup = BeautifulSoup(res.content, "lxml")
    for a in soup.find_all("a", attrs={"class": "bloko-link"}):
        vacancy_link = f'https://hh.ru{a.attrs["href"]}'
        print(type(vacancy_link))
        if vacancy_link.__contains__("negotiation_list"):
            print(vacancy_link)

    return

def get_data(ua, filename):
    data = []
    links = json_file_to_dict(filename)
    for page in links:
        time.sleep(1)
        print(page)
        print(links[page])
        res = requests.get(url=links[page], headers={"user-agent": ua.random})
        print(res)
        if res.status_code != 200:
            print("[SYS] Error in get_links(): status code not 200")
            return
        soup = BeautifulSoup(res.content, "lxml")
        try:
            try:
                company = soup.find("div", attrs={"class": "vacancy-company-details"})
            except:
                company = ""
            print(company)
            # try:
            #     vacancy = soup.find(attrs={"class": "resume-block__title-text"}).text
            # except:
            #     vacancy = ""
            # try:
            #     salary = soup.find(attrs={"class": "resume-block__title-text"}).text
            # except:
            #     salary = ""
            # try:
            #     tags = soup.find(attrs={"class": "resume-block__title-text"}).text
            # except:
            #     tags = ""
            # try:
            #     link = links[page]
            # except:
            #     link = ""
            # resume = {
            #     "company": company,
            #     "vacancy": vacancy,
            #     "salary": salary,
            #     "tags": tags,
            #     "link": link,
            # }
            # data.append(resume)
            print(data)
        except Exception as e:
            logging.error(e)
    with open(filename+"-data", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return


if __name__ == "__main__":
    ua = fake_useragent.UserAgent()
    # links = get_links(ua, "python") #ВОЗВРАЩАЕТ СПИСОК ССЫЛОК ПО ЗАДАННОЙ СПЕЦИАЛИЗАЦИИ
    # write_list_to_json_file(links, 'links.json') #записывает список в файл json
    # links = json_file_to_dict('links.json') #конвертирует данные из файла в дикт
    #print(json_file_to_dict('links.json')) #
    #authorized_request() #ПРИНТУЕТ ССЫЛКИ на странице "ОТКЛИКИ И ПРЕДЛОЖЕНИЯ"
    get_data(ua, 'links.json')



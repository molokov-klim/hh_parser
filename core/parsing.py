from os import name
import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import datetime
import json
import logging
from config import HH_HEADERS
from core.crud_files import CRUD

crud = CRUD()

class ParseHeadHunter:
    useragent = fake_useragent.UserAgent()

    # принимает string "наименование профессии", возвращает list со ссылками на вакансии
    # ["link1", "link2", "link3"]
    def vacancy_links(self, profession):
        links = []
        res = requests.get(
            url=f"https://hh.ru/search/vacancy?text={profession}&from=suggest_post&fromSearchLine=true&area=1&page=1&hhtmFrom=vacancy_search_list",
            headers={"user-agent": self.useragent.random}
        )
        if res.status_code != 200:
            logging.error("[SYS] Error in get_links(): status code not 200")
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
                        url=f"https://hh.ru/search/vacancy?text={profession}&from=suggest_post&fromSearchLine=true&area=1&page={page}&hhtmFrom=vacancy_search_list",
                        headers={"user-agent": self.useragent.random}
                    )
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.content, "lxml")
                        for a in soup.find_all("a", attrs={
                            "class": "bloko-link"}):
                            link = a.attrs["href"]
                            if link.__contains__("vacancy") and not link.__contains__("search"):
                                links.append(link)
                except Exception as e:
                    logging.error(e)
                print("page: ", page)
                #print("links:", links)
                time.sleep(1)
        except Exception as e:
            logging.error(e)
        return links


    # принимает String "наименование файла" со списком сссылок на вакансии, возвращает список с диктами
    # [{
    # "company": "company_name",
    # "vacancy": "vacancy_name",
    # "salary": "salary_qty",
    # "tags": ["tag1", "tag2", "tag3"],
    # "link": "link"
    # },]
    def vacancy_data(self, filename):
        result = {}
        data = json.loads(crud.read(filename))
        for link in data:
            res = requests.get(
                url=link,
                headers={"user-agent": self.useragent.random}
            )
            if res.status_code != 200:
                logging.error("[SYS] Error in get_links(): status code not 200")
                print("[SYS] Error in get_links(): status code not 200")
                return
            soup = BeautifulSoup(res.content, "lxml")






        return result









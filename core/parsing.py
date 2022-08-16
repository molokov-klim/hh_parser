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

    # принимает string "наименование профессии" (ТОЛЬКО ЛАТИНИЦА - HH переводит в транслит), возвращает list со ссылками на вакансии
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
                        url=f"https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text={profession}&clusters=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list",
                        headers={"user-agent": self.useragent.random}
                    )
                    if res.status_code == 200:
                        soup = BeautifulSoup(res.content, "lxml")
                        for a in soup.find_all("a", attrs={
                            "class": "bloko-link"}):
                            link = a.attrs["href"]
                            if link.__contains__("https://hh.ru/vacancy/"):
                                links.append(link)
                    #print(links)
                except Exception as e:
                    logging.error(e)
                print("page: ", page)
                # print("links:", links)
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
    def vacancy_data(self, filename_input, filename_output):
        try:
            crud.delete(filename_output)
        except:
            pass
        data = json.loads(crud.read(filename_input))
        print(len(data))
        for link in data:
            print(data.index(link))
            res = requests.get(
                url=link,
                headers={"user-agent": self.useragent.random}
            )
            if res.status_code != 200:
                logging.error("[SYS] Error in get_links(): status code not 200")
                print("[SYS] Error in get_links(): status code not 200")
                return
            soup = BeautifulSoup(res.content, "lxml")
            try:
                company = soup.find("div", attrs={"class": "vacancy-company-details"}).find("span").find("a").find(
                    "span").text
            except:
                company = ""
            try:
                vacancy = soup.find("div", attrs={"class": "vacancy-title"}).find("h1").text
            except:
                vacancy = ""
            try:
                salary = soup.find("div", attrs={"data-qa": "vacancy-salary"}).find("span").text
            except:
                salary = ""
            try:
                tags = [tag.text.replace("\u2009", "").replace("\xa0", " ") for tag in
                        soup.find(attrs={"class": "bloko-tag-list"}).find_all("span", attrs={
                            "data-qa": "bloko-tag__text"})]
            except:
                tags = ""

            resume = {
                "company": company.replace("\u2009", "").replace("\xa0", " "),
                "vacancy": vacancy.replace("\u2009", "").replace("\xa0", " "),
                "salary": salary.replace("\u2009", "").replace("\xa0", " "),
                "tags": tags,
                "link": link,
            }
            crud.append_to_json(filename_output, resume)
            time.sleep(1)
        return True

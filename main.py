from os import name
import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import datetime
import json
import logging
from config import HH_HEADERS
from core.parsing import ParseHeadHunter
from core.crud_files import CRUD
from core.analysis import Analysis

parse = ParseHeadHunter()
crud = CRUD()
analyze = Analysis()


def init():
    vacancy_links_filename = 'vacancy_links.json'
    vacancy_data_filename = 'vacancy_data.json'

    # -------------ПАРСИНГ ССЫЛОК НА ВАКАНСИИ----------------------------------
    # links = parse.vacancy_links("QA")
    # if crud.create(vacancy_links_filename):
    #     crud.update(vacancy_links_filename, links)
    # else:
    #     print("File already exist")

    # -------------ПАРСИНГ ДАННЫХ ИЗ ВАКАНСИИ----------------------------------
    # parse.vacancy_data(vacancy_links_filename, vacancy_data_filename)

    # -------------АНАЛИЗ ДАННЫХ ИЗ ВАКАНСИИ----------------------------------
    for k, v in analyze.get_skills(vacancy_data_filename, 0.01).items():
        print(k, v)

    return


if __name__ == "__main__":
    init()

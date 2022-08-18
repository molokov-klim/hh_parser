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
    analysys_vacancy_data_filename = 'analysys_vacancy_data.txt'
    resume_vacancy_links_filename = 'resume_vacancy_links.json'

    # -------------ПАРСИНГ ССЫЛОК НА ВАКАНСИИ----------------------------------
    # links = parse.vacancy_links("QA")
    # if crud.create(vacancy_links_filename):
    #     crud.update(vacancy_links_filename, links)
    # else:
    #     print("File already exist")

    # -------------ПАРСИНГ ДАННЫХ ИЗ ВАКАНСИИ----------------------------------
    # parse.vacancy_data(vacancy_links_filename, vacancy_data_filename)

    # -------------АНАЛИЗ ДАННЫХ ИЗ ВАКАНСИИ----------------------------------
    tag = analyze.analyze_vacancy_data(vacancy_data_filename, 0.01)
    crud.update(analysys_vacancy_data_filename, tag)

    # -------------WHO AM I----------------------------------
    print("me: ", parse.who_am_i())

    # -------------ПАРСИНГ ССЫЛОК НА ВАКАНСИИ ПО РЕКОММЕНДАЦИЯМ К РЕЗЮМЕ----------------------------------
    # links = parse.resume_vacancy_links()
    # print(links)
    # if crud.create(resume_vacancy_links_filename):
    #     crud.update(resume_vacancy_links_filename, links)
    # else:
    #     print("File already exist")

    # -------------ОТКЛИК НА ВАКАНСИЮ----------------------------------
    parse.respond_vacancy("https://hh.ru/vacancy/68451749?from=vacancy_search_list&hhtmFrom=vacancy_search_list")






    return


if __name__ == "__main__":
    init()

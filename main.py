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

parse = ParseHeadHunter()
crud = CRUD()

def init():
    #-------------ПАРСИНГ ССЫЛОК НА ВАКАНСИИ----------------------------------
    vacancy_links_filename = 'links.json'
    # links = parse.vacancy_links("Тестировщик")
    # if crud.create(vacancy_links_filename):
    #     crud.update(vacancy_links_filename, links)
    # else:
    #     print("File already exist")

    # -------------ПАРСИНГ ДАННЫХ ИЗ ВАКАНСИИ----------------------------------
    vacancy_data = parse.vacancy_data(vacancy_links_filename)
    print("vacancy_data: ", vacancy_data)

    return








if __name__ == "__main__":
    init()




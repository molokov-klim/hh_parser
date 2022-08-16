import os
import json


class CRUD:

    # принимает String "наименование_файла", если файл существует возвращает False, если нет - создает его и возвращает True
    def create(self, filename):
        if os.path.isfile(filename):
            return False
        else:
            fp = open(filename, 'x')
            fp.close()
            return True

    def update(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def read(self, filename):
        if not os.path.isfile(filename):
            print("File not exist")
            return False
        with open(filename) as f:
            lines = f.read()
        return lines






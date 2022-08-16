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
        return

    def append_to_json(self, filename, data):
        print("append_to_json ", filename, " ", data)
        if not os.path.isfile(filename):
            f = open(filename, 'x')
            f.write("[")
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.write("]")
            f.close()
        if os.path.isfile(filename):
            with open(filename, 'a') as f:
                truncate_utf8_chars(filename, 1)
                f.write(", ")
                json.dump(data, f, ensure_ascii=False, indent=4)
                f.write("]")
        return

    def read(self, filename):
        if not os.path.isfile(filename):
            print("File not exist")
            return False
        with open(filename) as f:
            lines = f.read()
        return lines

    def delete(self, filename):
        os.remove(filename)



def truncate_utf8_chars(filename, count, ignore_newlines=True):
    """
    Truncates last `count` characters of a text file encoded in UTF-8.
    :param filename: The path to the text file to read
    :param count: Number of UTF-8 characters to remove from the end of the file
    :param ignore_newlines: Set to true, if the newline character at the end of the file should be ignored
    """
    with open(filename, 'rb+') as f:
        last_char = None

        size = os.fstat(f.fileno()).st_size

        offset = 1
        chars = 0
        while offset <= size:
            f.seek(-offset, os.SEEK_END)
            b = ord(f.read(1))

            if ignore_newlines:
                if b == 0x0D or b == 0x0A:
                    offset += 1
                    continue

            if b & 0b10000000 == 0 or b & 0b11000000 == 0b11000000:
                # This is the first byte of a UTF8 character
                chars += 1
                if chars == count:
                    # When `count` number of characters have been found, move current position back
                    # with one byte (to include the byte just checked) and truncate the file
                    f.seek(-1, os.SEEK_CUR)
                    f.truncate()
                    return
            offset += 1
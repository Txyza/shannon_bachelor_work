#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============
#      Date: 03.12.2016
#       Author: Chusovitin Anton Romanovich
# ==============

import re
import requests
import wget
import os
from pyunpack import Archive
import time

def req():      # Рекурсивный обход сайта
    site = "http://www.knigitxt.com/"
    for i in range(10, 31):
        print(i)
        data = requests.get("http://www.knigitxt.com/authors/all/"+str(i))
        authors = re.findall("/author/\d{1,5}", data.text)
        for author in authors:
            data = requests.get("http://www.knigitxt.com" + author)
            books = re.findall("/preview/[A-Za-z0-9_()-]{1,350}.html", data.text)
            for book in books:
                data = requests.get("http://www.knigitxt.com"+book)
                downloads = re.findall("/download/\d{1,10}.html", data.text)
                for download in downloads:
                    data = requests.get("http://www.knigitxt.com" + download)
                    rars = re.findall("/media/\w{1,100}/[A-Za-z0-9_%()-]{1,100}/[A-Za-z0-9_%()-]{1,100}.rar", data.text)
                    for rar in rars:
                        print(author, " ", book, " ", download, " ", rar)
                        file = wget.download("http://www.knigitxt.com"+rar)
                        time.sleep(0.1)
                        Archive(file).extractall('text/')
                        os.remove(file)


if __name__ == '__main__':
    req()
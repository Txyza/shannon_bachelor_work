#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============
#      Date: 03.12.2016
#       Author: Chusovitin Anton Romanovich
# ==============

import re
import requests
import zipfile
#pip install
import wget
#pip install
from pyunpack import Archive
from unrar import rarfile

def downloads():    # Загрузка zip архива и распаковка файла
    pass

def rename(name):   # Сменить имя файла на md5(от имени)
    pass

def req():      # Рекурсивный обход сайта
    site = "http://www.knigitxt.com/"
    for i in range(1, 31):
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
                        file = wget.download("http://www.knigitxt.com"+rar)
                        #rarfile.RarFile(file).extractall()

                        with rarfile.RarFile(file) as rf:
                            for f in rf.infolist():
                                print(f.filename)
                                with open(f.filename, "wb") as of:
                                    of.write(rf.read(f))

                        print(rar, " ", file)


if __name__ == '__main__':
    req()
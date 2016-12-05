#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============
#      Date: 04.12.2016
#       Author: Chusovitin Anton Romanovich
# ==============


import os
import hashlib

def rename():

    for name in os.listdir("text/"):
        newName = hashlib.md5()
        newName.update(name.encode())
        os.rename("text/"+name, "textCode/"+newName.hexdigest()+".txt")


if __name__ == '__main__':
    rename()
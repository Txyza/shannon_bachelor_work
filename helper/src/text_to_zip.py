import subprocess
import os

list_dir = os.listdir('./../test')
for i in list_dir:
    a = subprocess.call('"C:\\Program Files\\WinRAR\\WinRAR.exe" a "C:\\project\\shannon_bachelor_work\\helper\\temp\\{0}.rar" "C:\\project\\shannon_bachelor_work\\helper\\test\\{0}"'.format(i), shell=True)

from os import listdir
from re import findall


files = listdir('log_test/single')
result = {}

index = 1
for file in files:
    with open('log_test/single/{}'.format(file), 'r') as f:
        data = f.read()
        test = findall(r'(True|False [\d]+ [\w]*)', data)
        result[index] = test
        index += 1

trues = {}
lens = {}
keys_file = {}
not_keys_file = {}
for key in result.keys():
    # Сколько успешно пройденных тестов
    trues[key] = len([_ for _ in result[key] if _ == 'True'])
    # Сколько всего тестов было в комплекте
    lens[key] = len([_ for _ in result[key]])
    # Сколько тестов было взломано файлами не из списка ключей
    not_keys_file[key] = len([_ for _ in result[key] if _[-5:] == 'False'])
    # Сколько тестов было взломано файлами из списка ключей
    keys_file[key] = len([_ for _ in result[key] if _[-4:] == 'True' and len(_) > 4])
    print(key, trues[key], lens[key], lens[key] / 100, trues[key] / (lens[key] / 100), keys_file[key], not_keys_file[key])

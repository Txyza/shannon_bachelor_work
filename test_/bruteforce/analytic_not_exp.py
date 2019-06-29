from os import listdir
from re import findall


files = listdir('log_test/not_exp')
result = {}
true = {}
false = {}

index = 1
for file in files:
    with open('log_test/not_exp/{}'.format(file), 'r') as f:
        file_index = int(file.split('_')[-1])
        for line in f.readlines():
            if line == 'True\n':
                true[file_index] = 0 if file_index not in true else true[file_index] + 1
            else:
                false[file_index] = 0 if file_index not in false else false[file_index] + 1
# print(false[9] / (true[9] + false[9]))
# print(true)
for key in sorted(false.keys()):
    print('%d %f %f' % (key, 100 - false[key] / (true[key] + false[key]) * 100, false[key] / (true[key] + false[key]) * 100))
    # print('%f' % falses if falses < 5 else falses - 1)
    # print('%f' % (100 - false[key] / (true[key] + false[key]) * 100))
    # print(key)

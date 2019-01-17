ch = 0
for k in range(1000):   # кол-во запусков
    for i in range(0, 100): # кол-во файлов
        for j in range(i+1, 100): # кол-во файлов
            ch += 1

print(ch)

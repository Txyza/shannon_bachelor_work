sum = 0;    minn = 100;     maxx = 0;   count = 0
file = open("statistics_bits128.txt", "r")

for line in file.readlines():
    line = int(line)
    count += 1
    sum += line
    minn = min(line, minn)
    maxx = max(line, maxx)
file.close()
print(count)
print(sum/count)
print(minn)
print(maxx)
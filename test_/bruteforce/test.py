from src.protocol.src.shannon import Shannon
from test.book.check import BookStack


def xor(answer, text):
    for i in range(len(answer)):
        answer[i] = answer[i] ^ text[i % 1024]
    return answer


def double_files(files):
    data, double_keys = [], []
    for first in range(len(files)):
        for second in range(first + 1, len(files)):
            with open("%s" % first, 'r') as f:
                data.append(bytearray(f.read()))
            with open("%s" % second, 'r') as f:
                data.append(bytearray(f.read()))
            double_keys.append(xor(data[0], data[1]))
    return double_keys


def single_files(files):
    single_key = []
    for file in files:
        with open("%s" % file, 'r') as f:
            single_key.append(bytearray(f.read()))
    return single_key


def get_result(mode, session, supposed_key, input_data):
    xor_result = xor(input_data, supposed_key)
    check_result = BookStack().check(xor_result)
    with open(r"log_test\%s\session_%s" % (mode, session), 'a') as f:
        f.write(check_result)


def run_test(input_data):
    for session in range(5):
        cipher, files, keys = Shannon().encode(input_data)
        input_data = bytearray(input_data.encode())
        print(keys)
        for supposed_key in single_files(files):
            get_result('single', session, supposed_key, input_data)
        for supposed_key in double_files(files):
            get_result('double', session, supposed_key, input_data)

run_test('1234567')
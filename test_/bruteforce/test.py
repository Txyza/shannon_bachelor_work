import sys
import os
from random import choice
from src.protocol.src.shannon import Shannon
from test_.book.check import BookStack
from itertools import combinations
from string import ascii_uppercase, ascii_lowercase, digits, hexdigits, whitespace, ascii_letters, punctuation


class Bruteforce:
    def __init__(self):
        # Количество сессий тестирования
        self.count_session = 100
        # Номер сессии
        self.session = None
        # количество файлов для тестирования
        self.count_files = 1
        # Выбранные файлы сессии
        self.files = None
        # Файлы ключей сессии используемые для шифрования
        self.keys = None
        # Файл для результата тестирования
        self.test_file = 'brute_file'
        # Название выходного файла
        self.out_file_name = ''
        # Количество тестов стопка книг
        self.N = 1
        self.string = ascii_uppercase+ascii_lowercase+digits+hexdigits+whitespace+ascii_letters+punctuation
        self.list_dir = os.listdir('./code')

    @staticmethod
    def xor(answer, text):
        if text:
            for i in range(len(answer)):
                answer[i] = answer[i] ^ text[i % len(text)]
        return answer

    def double_files(self, files):
        data, double_keys = [], []
        for first in range(1, len(files)+1):
            for second in range(first + 1, len(files)+1):
                with open(r"../../helper/text/%s" % first, 'rb') as f:
                    data.append(bytearray(f.read()))
                with open(r"../../helper/text/%s" % second, 'rb') as f:
                    data.append(bytearray(f.read()))
                double_keys.append(self.xor(data[0], data[1]))
        return double_keys

    @staticmethod
    def single_files(files):
        single_key = []
        for file in files:
            with open(r"../../helper/text/%s" % file, 'rb') as f:
                single_key.append(bytearray(f.read()))
        return single_key

    def _code_text(self, text, code):
        if isinstance(text, bytes):
            text = bytearray(text)
        return self.xor(text, code)

    def _make_key(self, exploit):
        """
        Метод из множества ключей формирует выходной ключ
        :param exploit:
        :return:
        """
        new_key = bytearray()
        for key in exploit:
            with open('%s\\..\\..\\helper\\text\\%s' % (sys.path[0], key), 'rb') as file_exploit:
                text_exploit = bytearray(file_exploit.read())
                new_key = self._code_text(text_exploit, new_key)
        return new_key

    def _make_exploit(self, exploit):
        """
        Метод формирует из множества ключей шифр последовательность
        :param exploit:
        :return:
        """
        if isinstance(exploit, str):
            exploit = [exploit]
        return self._make_key(exploit)

    def _code_file(self, file_in, file_out, exploit):
        text_exploit = self._make_exploit(exploit)
        with open('%s\\%s' % (sys.path[0], self.test_file), 'wb') as file_result:
            with open('%s' % file_out, 'rb') as file_code:
                while True:
                    text = file_code.read(1024)
                    if text == b'':
                        break
                    text = self._code_text(text, text_exploit)
                    file_result.write(text)

    def _switch(self, text, file_in=None, file_out=None, exploit=None):
        text_out = None
        if file_in and file_out and exploit:
            self._code_file(file_in, file_out, exploit)
        elif text and exploit and isinstance(exploit, str):
            text_out = self._code_text(text, exploit)
        return text_out

    def get_result(self, mode, check_status, exploit, info=None, file_in=None):
        f = file_in or open(r"log_test/%s/session_%s_%s" % (mode, self.out_file_name, self.session), 'a')
        if info:
            f.write('Тест: {}\n'.format(info))
        if not check_status and mode == 'single':
            f.write('%s %s %s\n' % (
                str(check_status),
                str(exploit),
                str('..\\..\\helper\\text\\'+exploit in self.keys)
            ))
        elif not check_status and mode != 'single':
            f.write('%s %s\n' % (
                str(check_status),
                str(exploit)
            ))
        else:
            f.write('%s\n' % str(check_status))

    def _brute_all(self, text, file_in, file_out, count_files_key=4, session=1):
        """
        Методя для перебора всех файлов, входящих в список файлов сессии
        :param text:
        :param file_in:
        :param file_out:
        :return:
        """
        self.session = session
        # print('-' * 30)
        # print('Запуск сессии "%d"' % session)
        self.out_file_name = file_out.split('\\')[-1]
        self.test_file = 'temp\\test_%s' % self.out_file_name
        cipher, self.files, self.keys = Shannon(count_files_key).encode(text, file_in, file_out)
        with open(r"log_test/%s/session_%s_%s_keys_%d" % ('single', self.out_file_name, self.session, count_files_key), 'a') as f:
            f.write('\n\nЗапуск сессии {}\n'.format(session))
            for exploit in self.files:
                # print('-' * 30)
                # print('Взлом файлом номер "%s"' % exploit)
                # if '..\\..\\helper\\text\\{}'.format(exploit) in self.keys:
                # print('Файл входит в последовательность, которой шифровали')
                # else:
                # print('Файл не входит в последовательность, которой шифровали')
                self._switch(text, file_in, file_out, exploit)
                self._check_result(exploit, 'single', f)

    def _test_not_exploit(self, text, file_in, file_out, count_files_key=4, session=1):
        """
        Методя для шифрования и проверки исходной последовательности
        :param text:
        :param file_in:
        :param file_out:
        :return:
        """
        self.session = session
        self.out_file_name = file_out.split('\\')[-1]
        self.test_file = 'temp\\test_%s' % self.out_file_name
        cipher, self.files, self.keys = Shannon(count_files_key).encode(text, file_in, file_out)
        with open(r"log_test/%s/session_keys_%d" % ('not_exp', count_files_key), 'a') as f:
            check_result = BookStack().check(file=file_out)
            print(check_result)
            self.get_result('not_exp', check_result[1], '', None, f)

    def _brute_key_file(self, text, file_in, file_out, count_files_key=4, session=1):
        """
        Метод для перебора файлов, входящих в список ключей
        :param text:
        :param file_in:
        :param file_out:
        :return:
        """
        self.session = session
        # print('-' * 30)
        # print('Запуск сессии "%d"' % session)
        self.out_file_name = file_out.split('\\')[-1]
        self.test_file = 'temp\\test_%s' % self.out_file_name
        cipher, self.files, self.keys = Shannon(count_files_key).encode(text, file_in, file_out)
        with open(r"log_test/%s/session_%s_%s_keys_%d" % ('key', self.out_file_name, self.session, count_files_key), 'a') as f:
            f.write('\n\nЗапуск сессии {}\n'.format(session))
            for exploit in self.keys:
                # print('-' * 30)
                # print('Взлом ключевым файлом "%s"' % exploit)
                self._switch(text, file_in, file_out, exploit)
                self._check_result(exploit, 'key', f)

    def _brute_keys_files(self, text, file_in, file_out, count_files_key=4, count_exploit_file=1, session=1):
        """
        Метод для перебора нескольких файлов, входящих в список ключей
        :param text:
        :param file_in:
        :param file_out:
        :return:
        """
        self.session = session
        # print('-' * 30)
        # print('Запуск сессии "%d"' % session)
        self.out_file_name = file_out.split('\\')[-1]
        self.test_file = 'temp\\test_%s' % self.out_file_name
        cipher, self.files, self.keys = Shannon(count_files_key).encode(text, file_in, file_out)
        for i in range(len(self.files)):
            self.files[i] = '..\\..\\helper\\text\\' + self.files[i]
        for i in range(0, count_files_key+1):
            file_decode = list(self.keys)[:i] + self.files[:count_files_key-i]
            with open(r"log_test/%s/session_%s_%s_key_%d_keys_%d_other_%d" %
                      ('key', self.out_file_name, self.session, count_exploit_file, i, count_files_key-i), 'a') as f:
                # f.write('\n\nЗапуск сессии {}\n'.format(session))
                for exploit in combinations(file_decode, count_exploit_file):
                    # print('-' * 30)
                    # print('Взлом набором ключевых файлов "%s"' % str(exploit))
                    self._switch(text, file_in, file_out, exploit)
                    self._check_result(exploit, 'key', f)

    def _check_result(self, exploit, path='single', file_in=None):
        """
        Метод запускает N раз тестирование последовательности, для получения точного результата
        :param exploit:
        :return:
        """
        for i in range(self.N):
            check_result = BookStack().check(file=self.test_file)
            # print('Тестирование завершено, результат: ', check_result)
            # if check_result[1]:
            # print('Последовательность случайна')
            # else:
            # print('Последовательность неслучайна')
            info = None
            if isinstance(exploit, str):
                if '..\\..\\helper\\text\\{}'.format(exploit) in self.keys:
                    info = 'Файл {} входит в последовательность, которой шифровали'.format(exploit)
                else:
                    info = 'Файл {} не входит в последовательность, которой шифровали'.format(exploit)
            self.get_result(path, check_result[1], exploit, info, file_in)

    def test(self, text, file_in=None, file_out=None):
        """
        Метод для запуска теста брутфорса
        :param text:
        :param file_in:
        :param file_out:
        :return:
        """
        if text:
            text = bytearray(text.encode())
        for count_files_key in range(40, 50, 2):
            for session in range(self.count_session):
                file_in = './code/' + choice(self.list_dir)
                print(file_in)
                self.session = session
                # print('-' * 30)
                # print('Запуск сессии "%d" с ключами %d' % (session, count_files_key))
                # count_files_key = 5
                # Запуск брутфорса по всем файлам
                # self._brute_all(text, file_in, file_out, count_files_key, session)
                # Проверка исходной последовательности
                self._test_not_exploit(text, file_in, file_out, count_files_key, session)
                # Запуск с 1 ключевым файлом
                # self._brute_key_file(text, file_in, file_out, count_files_key, session)
                # Запуск с N ключевых файлов
                # count_exploit_file = count_files_key
                # self._brute_keys_files(text, file_in, file_out, count_files_key, count_exploit_file, session)
                # print('Окончание сессии "%d"' % session)

    def create_files(self):
        with open('test', 'w') as f:
            f.write(''.join([choice(self.string) for _ in range(5000000)]))

    @staticmethod
    def check_files():
        import os
        for path in os.listdir('../../helper/text'):
            path = '../../helper/text/' + path
            if not BookStack().check(file=path)[1]:
                print(path)
                os.remove(path)


if __name__ == '__main__':
    _text = None
    _file_in = '%s\\test' % sys.path[0]
    _out_name = ''.join([choice(ascii_lowercase) for i in range(10)])
    _file_out = '%s\\temp\\%s' % (sys.path[0], _out_name)
    Bruteforce().test(_text, _file_in, _file_out)

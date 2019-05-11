import sys
from random import choice
from string import ascii_lowercase
from src.protocol.src.shannon import Shannon
from test_.book.check import BookStack


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

    @staticmethod
    def xor(answer, text):
        for i in range(len(answer)):
            answer[i] = answer[i] ^ text[i % 1024]
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

    def single_files(self, files):
        single_key = []
        for file in files:
            with open(r"../../helper/text/%s" % file, 'rb') as f:
                single_key.append(bytearray(f.read()))
        return single_key

    def _code_text(self, text, code):
        if isinstance(text, bytes):
            text = bytearray(text)
        return self.xor(text, code)

    def _code_file(self, file_in, file_out, exploit):
        with open('%s\\..\\..\\helper\\text\\%s' % (sys.path[0], exploit), 'rb') as file_exploit:
            text_exploit = bytearray(file_exploit.read())
            with open('%s\\%s' % (sys.path[0], self.test_file), 'wb') as file_result:
                with open('%s' % (file_out), 'rb') as file_code:
                    while True:
                        text = file_code.read(1024)
                        if text == b'':
                            break
                        text = self._code_text(text, text_exploit)
                        file_result.write(text)

    def _switch(self, text, file_in=None, file_out=None, exploit=None):
        text_out = None
        if file_in and file_out and exploit:
            text_out = self._code_file(file_in, file_out, exploit)
        elif text and exploit and isinstance(exploit, str):
            text_out = self._code_text(text, exploit)
        return text_out

    def get_result(self, mode, check_status, exploit, info=None):
        with open(r"log_test/%s/session_%s_%s" % (mode, self.out_file_name, self.session), 'a') as f:
            if info:
                f.write('Тест: {}\n'.format(info))
            if not check_status:
                f.write('%s %s %s\n' % (str(check_status), str(exploit), str('..\\..\\helper\\text\\'+exploit in self.keys)))
            else:
                f.write('%s\n' % str(check_status))

    def _brute(self, text, file_in, file_out):
        for exploit in self.files:
            print('-' * 30)
            print('Взлом файлом номер "%s"' % exploit)
            if '..\\..\\helper\\text\\{}'.format(exploit) in self.keys:
                print('Файл входит в последовательность, которой шифровали')
            else:
                print('Файл не входит в последовательность, которой шифровали')
            self._switch(text, file_in, file_out, exploit)
            self._check_result(exploit)

    def _check_result(self, exploit):
        """
        Метод запускает N раз тестирование последовательности, для получения точного результата
        :param exploit:
        :return:
        """
        check_result = BookStack().check(file=self.test_file)
        print('Тестирование завершено, результат: ', check_result)
        if check_result[1]:
            print('Последовательность случайна')
        else:
            print('Последовательность неслучайна')
        info = None
        if '..\\..\\helper\\text\\{}'.format(exploit) in self.keys:
            info = 'Файл {} входит в последовательность, которой шифровали'.format(exploit)
        else:
            info = 'Файл {} не входит в последовательность, которой шифровали'.format(exploit)
        self.get_result('single', check_result[1], exploit, info)

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
        for session in range(self.count_session):
            self.session = session
            print('-' * 30)
            print('Запуск сессии "%d"' % session)
            self.out_file_name = file_out.split('\\')[-1]
            cipher, self.files, self.keys = Shannon().encode(text, file_in, file_out)
            with open(r"log_test/%s/session_%s_%s" % ('single', self.out_file_name, self.session), 'a') as f:
                f.write('\n\nЗапуск сессии {}\n'.format(session))
            self._brute(text, file_in, file_out)
            print('Окончание сессии "%d"' % session)
            # for supposed_key in self.single_files(files):
            #     self.get_result('single', session, supposed_key, text)
            # for supposed_key in self.double_files(files):
            #     self.get_result('double', session, supposed_key, text)


if __name__ == '__main__':
    text = None
    file_in = '%s\\test2' % sys.path[0]
    out_name = ''.join([choice(ascii_lowercase) for i in range(10)])
    file_out = '%s\\%s' % (sys.path[0], out_name)
    Bruteforce().test(text, file_in, file_out)


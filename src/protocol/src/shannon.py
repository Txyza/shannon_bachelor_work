from random import seed, randint, choice
from os import listdir


class Shannon:
    def __init__(self, count_files_key=4):
        # Количество файлов для шифрования
        self.count_files = 1024
        # Список файлов для шифрования
        self.files_code = list()
        # Список файлов отобранных для сессии
        self.files = set()
        # путь до директории text
        self.helper_dir = '..\\..\\helper'
        # Ключ шифрования
        self.key = ''
        # Количество ключей для шифрования
        self.count_files_key = count_files_key

    def _selection(self, private_key=124124):
        """
        Метод для выбора файлов сессии и файлов для шифрования
        :param private_key:
        :return:
        """
        seed(private_key)
        self._selection_files()
        self._selection_files_code()

    def _selection_files(self):
        """
        Метод для формирования множества файлов для сессии
        :return:
        """
        file_list = listdir("%s\\text" % self.helper_dir)
        if len(file_list) < self.count_files:
            raise ('Ошибка', 'Нужно больше файлов для шифрования')
        self.files = set()
        while len(self.files) < self.count_files:
            self.files.add(choice(file_list))
        self.files = list(self.files)

    def _selection_files_code(self):
        """
        Метод выбирает файлы, которыми будет использовать для шифрования
        :param private_key:
        :return:
        """
        count_files = self.count_files_key
        self.files_code = set()
        while len(self.files_code) < count_files:
            self.files_code.add("%s\\text\\%s" % (self.helper_dir, choice(self.files)))

    @staticmethod
    def _xor_key(text, code):
        """
        Метод выполняет операцию XOR к 2 последовательностям bytearray
        :param text:
        :param code:
        :return:
        """
        for index in range(len(text)):
            text[index] = text[index] ^ code[index % len(code)]
        return text

    @staticmethod
    def _xor(text, code):
        """
        Метод выполняет операцию XOR к 2 последовательностям bytearray
        :param text:
        :param code:
        :return:
        """
        for index in range(len(text)):
            text[index] = text[index] ^ code[index % len(code)]
        return text

    def _make_code_key(self):
        """
        Метод формирует ключ шифрования
        :return:
        """
        for file in self.files_code:
            with open(file, 'rb') as f:
                code = bytearray(f.read())*2250
                if self.key:
                    self.key, code = (code, self.key) if len(code) > len(self.key) else (self.key, code)
                    self.key = self._xor(self.key, code)
                else:
                    self.key = code

    def _message_with_key(self, text):
        """
        Метод шифрует последовательность с ключом шифрования
        :param text:
        :return:
        """
        return self._xor(text, self.key)

    def _encode_message_with_files(self, text):
        """
        Метод шифрует последовательность рассчитывая ключ шифрования во время шифрования
        :param text:
        :return:
        """
        for file_code in self.files_code:
            with open(file_code, 'rd') as f:
                code = f.read(1024)
        return text

    def _code_text(self, text):
        if isinstance(text, bytes):
            text = bytearray(text)
        return self._message_with_key(text)

    @staticmethod
    def _open_file(file, mode='rb'):
        if isinstance(file, str):
            file = open(file, mode)
        return file

    def _code_file(self, file_in, file_out=None):
        file_in = self._open_file(file_in)
        file_out = self._open_file(file_out, 'wb') if file_out else None
        while True:
            text = file_in.read(1024)
            if text == b'':
                break
            text = self._code_text(text)
            if file_out:
                file_out.write(text)

    def _switch(self, text, file_in=None, file_out=None):
        text_out = None
        if file_in and not file_out:
            text_out = self._code_file(file_in), self.files, self.files_code
        elif file_in and file_out:
            text_out = self._code_file(file_in, file_out), self.files, self.files_code
        elif text:
            text_out = self._code_text(text), self.files, self.files_code
        return text_out

    def encode(self, text='', file_in=None, file_out=None):
        """
        Метод шифрует строку
        :param text:
        :param file_in:
        :param file_out:
        :return:
        """
        self._selection(randint(2**512, 2**1024))
        self._make_code_key()
        return self._switch(text, file_in, file_out)

    def decode(self, text, file_in=None, file_out=None):
        """
        Метод расшифровывает строку
        :param text:
        :param file_in:
        :param file_out:
        :return:
        """
        return self._switch(text, file_in, file_out)


'''
input_text = 'hello world'
s = Shannon()
text = s.encode(input_text)
print('encode', text)
text = s.decode(text)
print('decode', text)
'''

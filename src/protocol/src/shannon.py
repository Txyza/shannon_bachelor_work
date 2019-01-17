from random import seed, randint, choice
from os import listdir


class Shannon:
    def __init__(self):
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

    def _selection(self, private_key=124124):
        """
        Метод для выбора файлов сессии и файлов для шифрования
        :param private_key:
        :return:
        """
        self._selection_files()
        self._selection_files_code(private_key)

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

    def _selection_files_code(self, private_key=124124):
        """
        Метод выбирает файлы, которыми будет использовать для шифрования
        :param private_key:
        :return:
        """
        seed(private_key)
        count_files = randint(50, 101)
        self.files_code = set()
        while len(self.files_code) < count_files:
            self.files_code.add("%s\\text\\%s" % (self.helper_dir, choice(self.files)))

    @staticmethod
    def _xor(text, code):
        """
        Метод выполняет операцию XOR к 2 последовательностям bytearray
        :param text:
        :param code:
        :return:
        """
        for index in range(len(text)):
            text[index] = text[index] ^ code[index % 1024]
        return text

    def _make_code_key(self):
        """
        Метод формирует ключ шифрования
        :return:
        """
        for file in self.files_code:
            with open(file, 'rb') as f:
                code = bytearray(f.read())
                self.key = self._xor(self.key, code) if self.key else code

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

    def encode(self, text=''):
        """
        Метод шифрует строку
        :param text:
        :return:
        """
        text = bytearray(text.encode())
        self._selection(124124)
        self._make_code_key()
        return self._message_with_key(text), self.files, self.files_code

    def decode(self, text):
        """
        Метод расшифровывает строку
        :param text:
        :return:
        """
        text = bytearray(text)
        return self._message_with_key(text), self.files, self.files_code

'''
input_text = 'hello world'
s = Shannon()
text = s.encode(input_text)
print('encode', text)
text = s.decode(text)
print('decode', text)
'''

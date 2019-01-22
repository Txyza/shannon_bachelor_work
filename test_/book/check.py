import subprocess


class BookStack:
    def __init__(self):
        # Файл теста
        self.file_test = r'../book/test'
        # конфигурации ХИ-квадрат
        self.Q05 = 3.84146
        self.Q9 = 0.01579
        self.q = 0

    def _write_file(self, text):
        """
        bs.exe принимает на вход файл, поэтому пишем промежуточный результат в файл
        :param text:
        :return:
        """
        with open(self.file_test, 'wb') as f:
            f.write(text)

    def _call(self):
        """
        Метод вызывает процесс bs.exe для тестирования
        :return:
        """
        call = ['../book/bs.exe', '-f',
                'test',
                '-w', '8', '-u', '128', '-q']
        data = subprocess.check_output(call).decode()
        return data

    def _hi(self, text, result):
        """
        Метод проверяет, является ли строка случайной по условию Хи-квадрата
        :param text:
        :param result:
        :return:
        """
        if float(result) <= self.Q05:
            return text, True
        else:
            return text, False

    def _check(self, text):
        """
        Метод запускает процесс тестирования
        :param text:
        :return:
        """
        self._write_file(text)
        result = self._call()
        return self._hi(text, result)

    def check(self, text):
        """
        Метод принимает на вход строку, которую необходимо протестировать
        на выход возвращается результат тестирования
        :param text:
        :return:
        """
        return self._check(text)

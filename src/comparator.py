class Comparator:
    """
    Абстрактный класс Comparator служит прототипом для унаследованных от него
    классов сравнения. Содержит абстрактный метод compare(self, left, right),
    который следует переопределить в классе-наследнике
    """
    def __init__(self, order: int):
        """
        Выполняет инициализацию экземляра класса
        :param order: порядок сортировки, запрошенный пользоателем. Принимает
        значение 1, при порядке сортировки по возастанию, и зачение -1, при
        порядке сортировки по убыванию
        """
        self.order = order

    def compare(self, left, right):
        """
        Абстрактный метод сравнения строк
        :param left: первая сравниваемая строка
        :param right: вторая сравниваемая строка
        :return: должен возвращать результат сравнения: 1, если порядок строк
        верный; -1, если порядок строк неверный; 0, если строки равны.
        """
        pass

    def _comparing(self, one, two) -> int:
        """
        Простейший метод сравнения
        :param one: первый аргумент
        :param two: второй аргумент
        :return: если выбран прямой порядок сортировки, возвращает: 1, если
         первый аргумент больше второго; -1, если второй аргумент больше
         первого; 0, если аргументы равны. Если выбран обратный порядок
         сортировки, возвращает: -1, если первый аргумент больше второго; 1,
         если второй аргумент больше первого; 0, если аргументы равны.
        """
        return ((one < two) - (one > two)) * self.order


class TextStringsComparator(Comparator):
    """
    Класс TextStringsComparator служит для сравнение текстовых строк
    :param ALPHABET: константа для определения порядка сортировки кириллицы
    """

    ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
               'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def compare(self, left: str, right: str) -> int:
        """
        Переопределенный метод для сравнения текстовых строк
        :param left: первая сравниваемая строка
        :param right: вторая сравниваемая строка
        :return: результат сравнения: 1, если строки располагаются в верном
        порядке; -1, если строки расположены в неверном порядке; 0, если строки
        равны.
        """
        len_left = len(left)
        len_right = len(right)
        size = min(len_left, len_right)
        for i in range(size):
            result = self._compare_string_char(left[i], right[i])
            if result != 0:
                return int(result)
        if len_left == len_right:
            return 0
        else:
            return int((-1 if len_left > len_right else 1) * self.order)

    def _compare_string_char(self, left: str, right: str) -> int:
        """
        Приватный метод сравнения текстовых символов, поддерживающий кириллицу.
        :param left: символ первой строки
        :param right: символ второй стоки
        :return: результат сравнения: 1, если символ первой строки стоки в
        алфавите стоит раньше чем символ второй стоки; -1, если символ второй
        стоки в алфавите стоит раньше чем символ первой строки; 0, если символы
        идентичны
        """
        if left in self.ALPHABET and right in self.ALPHABET:
            return int(self._comparing(self.ALPHABET.index(left),
                                   self.ALPHABET.index(right)))
        else:
            return int(self._comparing(ord(left), ord(right)))


class IntegerStringsComparator(Comparator):
    """
    Класс IntegerStringsComparator служит для сравнениЯ числовых строк
    """
    def compare(self, left: int, right: int) -> int:
        """
        Переопределенный метод для сравнения числовых строк
        :param left: первая сравниваемая строка
        :param right: вторая сравниваемая строка
        :return: результат сравнения: 1, если порядок строк верный; -1, если
        порядок строк неверный; 0, если строки равны.
        """
        return int(self._comparing(left, right))

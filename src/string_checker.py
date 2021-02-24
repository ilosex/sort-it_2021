import re


class StringChecker:
    """
    Класс StringChecker служит для проверки содержимого входящих строк
    """
    def __init__(self, values_type: str, comparator) -> None:
        """
        Выполняет инициацию экземляра класса.
        :param values_type: values_type: тип строк, обозначенный пользователем
        :param comparator: объект класса Comparator. Служит для сравнения
        заданного типа строк
        """
        self.values_type = values_type
        self.comparator = comparator
        self.__regexp = self.regexp

    def check_string(self, old_string: str, string: str) -> bool:
        """
        Служит для проверки считанной строки string на соответствие заданным
        параметрам сортировки
        :param old_string: предыдущая валидная строка файла. Используется при
        проверке соответствия порядку сортировки
        :param string: проверяемая строка
        :return: True, если проверка пройдена и False в обратном случае
        """
        if string is None or string == '':
            return False
        return self._check_string_type(string) and \
               self._check_order(old_string, string)

    def _check_order(self, old_string: str, string: str) -> bool:
        """
        Выполняет проверку порядка сортировки входящего файла на соответствие
        заданному
        :param old_string: предыдущая валидная строка файла. Используется при
        проверке соответствия порядку сортировки
        :param string: проверяемая строка
        :return: True, если проверка пройдена и False в обратном случае
        """
        if old_string is None:
            return True
        result_compare = self.comparator.compare(old_string, string)
        return result_compare != -1

    def _check_string_type(self, string: str) -> bool:
        """
        Проверяет соответствие типа строки заданному
        :param string: проверяемая строка
        :return: True, если проверка пройдена и False в обратном случае
        """
        return len(re.findall(self.__regexp, string)) == 0

    @property
    def regexp(self) -> str:
        """
        Задает значение проверочного выражения в зависимости от заданного типа
        данных
        :return: регулярное выражение в соответствии с заявленным типом данных
        """
        if self.values_type == '-i':
            return r'\D'
        elif self.values_type == '-s':
            return r'\s'

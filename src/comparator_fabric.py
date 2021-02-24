from src import comparator


class ComparatorFabric:
    """
    Класс ComparatorFabric служит для автоматического подбора компаратора
    в зависимости от полученных от пользователя аргументов командной строки
    """
    def __init__(self, values_type: str, order: str) -> None:
        """
        Выполняет инициализацию экземляра класса
        :param values_type: тип строк, обозначенный пользователем
        :param order: порядок сортировки, запрошенный пользоателем. Принимает
        значение 1, при порядке сортировки по возастанию, и зачение -1, при
        порядке сортировки по убыванию
        """
        self.values_type = values_type
        self.order = order

    def give_me_comparator(self) -> object:
        """
        Метод сравнения строк поддерживаемых типов
        :return: компаратор для заданного типа строк
        """
        if self.values_type == '-s':
            return comparator.TextStringsComparator(self._get_order())
        elif self.values_type == '-i':
            return comparator.IntegerStringsComparator(self._get_order())

    def _get_order(self) -> int:
        """
        Приватный метод возвращающий цифровое обозначение для выбранного
        порядка сортировки
        :return: если выбран порядок сортировки по возрастанию, возвращает -1;
        если выбран порядок сортировки по убыванию, возвращает 1
        """
        if self.order == '-a':
            return 1
        elif self.order == '-d':
            return -1

from src import file


class FileFabric:
    """
    Класс FileFabric реализует возможность автоматического подбора необходимого
    типа объекта фойла для чтения или записи.
    """
    def __init__(self, path: str, mode: str) -> None:
        """
        Метод для инициализации класса
        :param path: путь файла
        :param mode: режим работы с файлом
        """
        self.path = path
        self.mode = mode

    def give_me_file(self):
        """
        Возвращает объект класса необходимого типа
        :return: Объект класса необходимого типа
        """
        if self.mode == 'r':
            return file.ReadFile(self.path)
        elif self.mode == 'w':
            return file.WriteFile(self.path)

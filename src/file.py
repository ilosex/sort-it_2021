import sys
import locale


class File:
    """
    Класс File предоставляет инструменты для работы с файлами
    """
    def __init__(self, path: str) -> None:
        """
        Инициализирует экземляр класса. При инициализации выбирается кодировка
        входных файлов в зависимости от локали системы.
        :param path: путь к файлу. Должен быть строкой.
        """
        self.path = path
        self.mode = None
        self.opened_file = None
        self.encoding = locale.getpreferredencoding()

    def _check_file(self) -> bool:
        """
        Метод служит для проверки файлов. Проверяется существование файла,
        права доступа, тип объекта по по указанному пути (файл или директория)
        и является ли введенная при инициализации объекта класса строка адресом
         файла
        :return: если при проверке не возникло ошибок, возвращает True,
        иначе - False
        """
        try:
            f = open(self.path, mode=self.mode)
            f.close()
            return True
        except FileNotFoundError:
            print(f'Файл {self.path} не существует!', file=sys.stderr)
            return False
        except IsADirectoryError:
            print(f'{self.path} - это директория!', file=sys.stderr)
            return False
        except TypeError as e:
            print(f'{self.path} не является путем файла:',
                  sys.stderr.write(*e.args), sep='\n')
        except PermissionError:
            print(f'Недостаточно прав для доступа к файлу {self.path}!',
                  file=sys.stderr)
            return False

    def open_file(self) -> object:
        """
        Возвращает объект открытого файла
        """
        self.opened_file = open(str(self.path),
                                mode=self.mode,
                                encoding=self.encoding)
        return self.opened_file


class ReadFile(File):
    """
    Класс ReadFile унаследован от класса File и используется для чтения файлов
    """
    def __init__(self, path: str) -> None:
        """
        Инициализирует экземляр класса
        :param path: путь к файцлу, который необходимо прочесть
        """
        super().__init__(path)
        self.mode = 'r'

    def check_file(self) -> bool:
        """
        Проверяет валидность файла
        :return: если при проверке не возникло ошибок, возвращает True,
        иначе - False
        """
        return super()._check_file()

    def read_line(self):
        """
        Считывает строку из файла. Если считываемая строка содержит символы,
        не принадлежищие юникоду или имеет место попытка считать строку из
        неоткрытого файла, возвращает None.
        :return: Считанную строку. Если при считывании строки возникли проблемы
         - None
        """
        if self.opened_file is not None:
            try:
                s = self.opened_file.readline().rstrip('\n')
                return s
            except UnicodeDecodeError:
                print(f'Строка в файле {self.path} имеет невалидные символы.'
                      f' Строка пропущена.', file=sys.stderr)
            return None
        else:
            print(f'Немогу считать строку: файл {self.path} не открыт')
            return None


class WriteFile(File):
    """
    Класс WriteFile унаследован от класса File и применяется для работы с
    записываемыми файлами.
    """
    def __init__(self, path: str) -> None:
        """
        Инициализирует экземляр класса
        :param path: путь к файлу
        """
        super().__init__(path)
        self.mode = 'w'

    def check_file(self) -> bool:
        """
        Проверяет валидность файла для записи. При возникновении ошибок
        прекращает работу программы
        :return: при удачной проверке файла возвращает True
        """
        return True if super()._check_file() \
            else sys.exit(f'При проверке выходного файла {self.path} возникли '
                          f'ошибки! Выполнение программы прекращено')

    def write_line(self, line: str) -> None:
        """
        Записывает стоку в выходной файл. При возникновении ошибок при записи
        останавливает выолнение программы
        :param line: Записываемая строка
        """
        if self.opened_file is not None:
            self.opened_file.writelines(str(line) + '\n')
        else:
            sys.exit(f'Не могу записать в файл {self.path}! Выполнение '
                     f'программы прекращено!')

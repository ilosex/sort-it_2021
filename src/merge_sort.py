import pathlib
from src import file


class Merger:
    """
    Класс Merger осуществляет сортировку входящих файлов и передает данные для
    записи в исходящий файл
    """
    def __init__(self, checker, comparator,
                 output_file: str, input_files: list) -> None:
        """
        Инициализирует экземляр класса
        :param checker: экземляр класса для проверки валидности строк
        :param comparator: экземпляр класса для сравнения строк
        :param output_file: выходной файл
        :param input_files: входные файлы
        """
        self.string_checker = checker
        self.comparator = comparator
        self.input_files = input_files
        self.output_file = output_file

    def merge_sort(self) -> str:
        """
        Осуществляет сортировку слиянием входящих файлов
        :return: путь к выходному файлу
        """
        files = self._check_input_files(self.input_files)
        if len(files) <= 2:
            self._merge(files)
            return self.output_file
        else:
            mid = len(self.input_files) // 2
            left = Merger(self.string_checker,
                          self.comparator,
                          self.output_file + '_l',
                          self.input_files[:mid]).merge_sort()
            right = Merger(self.string_checker,
                           self.comparator,
                           self.output_file + '_r',
                           self.input_files[mid:]).merge_sort()
            files = self._check_input_files([left, right])
            self._merge(files)
            pathlib.Path(left).unlink()
            pathlib.Path(right).unlink()
            return self.output_file

    def _check_input_files(self, paths: list):
        """
        Осуществляет проверку входных файлов на валидность. Удаляет из списка
        входящих файлов невалидные
        :param paths: пути входных файлов
        :return: список открытых входных файлов
        """
        files = []
        files_path = []
        for f in paths:
            temp = file.ReadFile(f)
            if temp.check_file():
                files.append(temp)
                files_path.append(f)
        self.input_files = files_path
        return files

    def _merge(self, input_files) -> None:
        """
        Осуществляет слияние содержимого входных файлов
        :param input_files: объекты открытых входных файлов
        """
        def save_and_give_next(out, inp, element: str) -> str:
            """
            Внутренняя вспомогательная функция для сохранения обработанной
            строки в выходной файл и выдачи следующей строки входного файла
            :param out: объект открытого выходного файла
            :param inp: объект открытого входного файла
            :param element: строка для сохранения в выходной файл
            :return: строку для сортировки
            """
            out.write_line(element)
            return self._give_next_valid_element(inp, element)

        output_file = file.WriteFile(self.output_file)
        output_file.check_file()

        if len(input_files) == 1:
            input_file = input_files[0]
            with input_file.open_file(), output_file.open_file():
                input_line = self._give_next_valid_element(input_file, None)
                while input_line:
                    output_file.write_line(input_line)
                    input_line = self._give_next_valid_element(input_file,
                                                               input_line)
        elif len(input_files) == 2:
            left = input_files[0]
            right = input_files[1]
            with left.open_file(), right.open_file(), output_file.open_file():
                old_element = None
                left_element = self._give_next_valid_element(left, old_element)
                right_element = self._give_next_valid_element(right,
                                                              old_element)
                while left_element and right_element:
                    c = self.comparator.compare(left_element, right_element)
                    if c == 1:
                        left_element = save_and_give_next(output_file,
                                                          left,
                                                          left_element)
                    else:
                        right_element = save_and_give_next(output_file,
                                                           right,
                                                           right_element)
                else:
                    while right_element:
                        right_element = save_and_give_next(output_file,
                                                           right,
                                                           right_element)
                    while left_element:
                        left_element = save_and_give_next(output_file,
                                                          left,
                                                          left_element)

    def _give_next_valid_element(self, inp, old_element: str or None) -> str:
        """
        Проверяет и выдает строку из входного файла
        :param inp: объект открытого входного файла
        :param old_element: последняя сохраненная в выходной файл строка
        входного файла
        :return: валидная строка входного файла
        """
        element = inp.read_line()
        while (not self.string_checker.check_string(old_element, element))\
                and element:
            element = inp.read_line()
        return element

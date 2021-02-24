import argparse


class ArgumentsParser:

    def parse(self):
        """
        Принимает аргументы командной строки и обрабатывает их. При
        несоответствии полученных элементов ТЗ останавливает выполнение
        программы и выводит сообщение об ошибке
        :return: возвращает словарь с опциями запуска программы.
        """

        description = '''Результатом работы программы является новый файл с 
        объединенным содержимым входных файлов, отсортированным по возрастанию 
        или убыванию путем сортировки слиянием.
        Программа сортирует только текстовые (String) или числовые (Integer) 
        данные.
        Если содержимое исходных файлов не позволяет произвести сортировку 
        слиянием (например, нарушен порядок сортировки), производится частичная 
        сортировка (сортируются только валидные данные).
        Выходной файл содержит отсортированные данные даже в случае ошибок, 
        однако возможна потеря ошибочных данных.'''

        def min_length(min_arguments_number: int):
            """
            Реализует проверку наличия аргументов в количистве не менее,
            заданного в min_arguments_number.
            :param min_arguments_number: минимально необходимое количество
            аргументов
            :return: возвращает ссылку на класс реализующий проверку
            """

            class RequiredLength(argparse.Action):
                """
                Внутренний класс, унаследованный от argparse.Action,
                реализующий проверку количества элементов с помощью
                переопределенного метода __call__
                """
                def __call__(self, parser, namespace,
                             values: str, option_string=None) -> None:
                    if not min_arguments_number <= len(values):
                        msg = f'Количество аргументов типа "{self.dest}" ' \
                              f'должно быть не менее {min_arguments_number}'
                        raise parser.error(message=msg)
                    setattr(namespace, self.dest, values)
            return RequiredLength

        args_parser = argparse.ArgumentParser(description=description,
                                              add_help=False)
        order = args_parser.add_mutually_exclusive_group(required=False)
        args_parser.add_argument('-h', '--help',
                                 action='help',
                                 default=argparse.SUPPRESS,
                                 help='Показывает это сообщение и закрывает'
                                      ' программу')
        order.add_argument('-a',
                           action='store_const',
                           const='-a',
                           dest='order',
                           default='-a',
                           help='необязательный атрибут, используйте для '
                                'сортировки по возрастанию (по умолчанию)')
        order.add_argument('-d',
                           action='store_const',
                           const='-d',
                           default='-a',
                           dest='order',
                           help='необязательный атрибут, используйте для '
                                'сортировки по убыванию')
        variable_type = args_parser.add_mutually_exclusive_group(required=True)
        variable_type.add_argument('-i',
                                   action='store_const',
                                   const='-i',
                                   dest='values_type',
                                   help='обязательный атрибут, используйте для'
                                        ' сортировки числовых данных')
        variable_type.add_argument('-s',
                                   action='store_const',
                                   const='-s',
                                   dest='values_type',
                                   help='обязательный атрибут, используйте для'
                                        ' сортировки текстовых данных')
        args_parser.add_argument('output_file',
                                 type=str,
                                 default='output.txt',
                                 help='обязательный атрибут, путь к выходному'
                                      ' файлу')
        args_parser.add_argument('input_files',
                                 nargs='+',
                                 action=min_length(1),
                                 help='обязательный атрибут, пути к входным'
                                      ' файлам. Требуется путь минимум одного '
                                      'файла')
        '''Следующие 2 строки содержат небольшой чит: обращение к приватным 
        элементам класса импортированной библиотеки, но без этого 
        переопределить название заголовков описания аргументов у меня сделать 
        не получилось.'''
        args_parser._positionals.title = 'Обязательные аргументы'
        args_parser._optionals.title = 'Необязательные аргументы'
        args = args_parser.parse_args()
        args = vars(args)
        dict_args = dict()
        [dict_args.update({key: value}) for key, value in args.items() if value
         is not None]
        return dict_args

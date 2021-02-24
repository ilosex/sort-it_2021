import pathlib
import sys

from src import parser, comparator_fabric, merge_sort, string_checker


def main() -> None:
    """
    Основная функция программы. Парсит аргументы командной строки с помощью
    ArgumentsParser(). Получает объект класса ComparatorFabric, который,
    методом give_me_comparator(), на основе полученных сведений о типе входных
    данных и порядке сортировки, возвращает объект классаTextStringsComparator
    или IntegerStringsComparator, умеющий сравнивать строки в соответствии с
    обозначенным порядком сортировки. На основе входных аргументов получает
    объект класса StringChecker, необходимы для провери валидности строк.
    Передает объекты чекера и компаратора для сборки объекта класса Merger,
    который непосредственно будет заниматься сортировкой входных файлов, а так
    же сохранением результата в выходной файл. С помощью созданного
    сортировщика сортирует переданное и выводит отчет об результатах своей
    деятельности.
    """
    pars = parser.ArgumentsParser()
    args = pars.parse()
    cf = comparator_fabric.ComparatorFabric(args['values_type'], args['order'])
    comparator = cf.give_me_comparator()
    checker = string_checker.StringChecker(args['values_type'], comparator)
    sorter = merge_sort.Merger(checker, comparator,
                               args['output_file'], args['input_files'])
    sorter.merge_sort()
    output_file = pathlib.Path(args['output_file'])
    script_name = pathlib.Path(__file__).name
    if output_file.stat().st_size == 0:
        output_file.unlink()
        print(f'К сожалению, программа {script_name} не обнаружила валидных '
              f'данных для сортировки.', file=sys.stderr)
    else:
        print(f'Программа {script_name} успешно завершила работу. '
              f'Отстортированные данные сохранены в файл '
              f'{str(output_file.absolute())}')


if __name__ == '__main__':
    main()

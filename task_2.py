import os
import datetime


def logger(path):

    def __logger(old_function):
        nonlocal path
        def new_function(*args, **kwargs):
            nonlocal path
            start = datetime.datetime.now().strftime('%d.%m.%Y %H:%m')
            name_func = old_function.__name__
            arguments = f'{args} {kwargs}'
            return_value = old_function(*args, **kwargs)
            data = (f'date and time: {start} \n'
                      f'function name: {name_func}\n'
                      f'arguments: {arguments}\n'
                      f'return value: {return_value}\n')

            with open(path, 'a', encoding='utf-8') as f:
                f.write(data)
            return return_value

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()

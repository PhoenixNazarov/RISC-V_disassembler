from functools import wraps


# def check_global_funct(func):
#     @wraps(func)
#     def wrap(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             print(f'Программа вызвала исключение {e}')
#             print(f'Не удалось отследить точное местоположение ошибки')
#             raise e
#     return wrap


def check_global_funct(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'The program has thrown an exception {e}')
            print(f'Could not track the exact location of the error')
            if func.__name__ == 'Elf32':
                print('Most likely the Elf32 class was misused')
            raise e
    return wrap


def check_exception(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        out = None
        try:
            out = func(*args, **kwargs)
        except (FileNotFoundError, FileExistsError):
            print("Cant open elf file")
            exit()
        except IncorrectData:
            print(f'{func.__name__:20}: elfError')
            exit()
        except TypeError:
            print(f'{func.__name__:20}: typeError')
            exit()
        except UnboundLocalError:
            print(f'{func.__name__:20}: hardError')
            exit()
        except Exception as e:
            print(e)
            print(f'{func.__name__:20}: error')
            exit()
        else:
            print(f'{func.__name__:20}: ok')
            return out

    return wrap


def check_algorithms(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'Algorithm {func.__name__} threw an exception {e}')
            raise e
    return wrap


def replace_unknown_data(name):
    def check_unknown_data(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return name
        return wrap
    return check_unknown_data

def check_command(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass
    return wrap


class IsCompressComandError(Exception):
    def __init__(self, row):
        print(f'Elf file incorrect value on row {row}')


class IncorrectData(Exception):
    def __init__(self, name, data):
        print(f'Elf file incorrect value {name}: {data}')


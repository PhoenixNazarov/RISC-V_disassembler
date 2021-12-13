def check_elf_reader_exception(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, FileExistsError):
            print("Cant open elf file")
            exit(0)
        except Incorrect_Data:
            exit()
        except Exception as e:
            raise e

    return wrap


class Incorrect_Data(Exception):
    def __init__(self, name, data):
        print(f'Incorrect value {name}: {data}')

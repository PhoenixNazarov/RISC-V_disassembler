from elf_parser.exceptions import check_exception, check_command, check_commandSc


@check_commandSc
class A:
    def __init__(self):
        self.ooo()

    def ooo(self):
        print(1/0)

b = A()
from . import format


def bytes_to_string(_bytes):
    return ''.join([chr(int(i, 16)) for i in _bytes])


class Elf32:
    __headers = {}
    __sections = []
    __names = []
    __symtab = []

    def add_headers(self, headers):
        self.__headers |= headers

    def add_sections(self, sections):
        self.__sections += sections

    def add_names(self, names):
        self.__names += names

    def add_symtab(self, symtab):
        self.__symtab += symtab

    def get_section_by_name(self, name):
        # if name in '.symtab':
        for i in range(len(self.__names)):
            if name == self.__names[i]:
                return dict(self.__sections[i])

    def get_string_symtab(self):
        form = "[{:>4}] {:15} {:>5} {:8} {:8} {:8} {:>6} {}\n"
        string = 'Symbol Value            Size Type     Bind     Vis       Index Name'
        index = 0
        for _sym in self.__symtab:
            sym = dict(_sym)
            if int(sym['SHNDX'], 16) in format.symtab_special.keys():
                sindex = format.symtab_special[int(sym['SHNDX'], 16)]
            else:
                sindex = int(sym['SHNDX'], 16)

            string += form.format(index,
                            sym["VALUE"],
                            int(sym["SIZE"], 16),
                            format.symtab_types[
                                int(sym['INFO'],
                                    16) & 15],
                            format.symtab_binds[
                                int(sym['INFO'],
                                    16) >> 4],
                            format.symtab_vises[
                                int(sym['OTHER'],
                                    16 & 3)],
                            sindex,
                            sym["PARSE_NAME"])
            index += 1
        return string

    def __getattr__(self, item):
        if item == "__headers":
            print('lpl')
            return self.__headers
        headers_key = format.math_e_ident.keys() | format.match_header_white_list.keys()
        if item in headers_key:
            return int(dict(self.__headers)[item], 16)
        return self.__dict__[item]


class CommandsBase:
    def __init__(self, _bytes):
        self.__bytes = _bytes
        self.__commands = []
        self.__index = 0

    def __get_next_block(self, _type):
        if _type == 'compress':
            yield self.__bytes[self.__index: self.__index + 2]
            self.__index += 2
        else:
            yield self.__bytes[self.__index: self.__index + 4]
            self.__index += 4

    def __parse_commands(self):
        while self.__index < len(self.__bytes):
            self.__parse_next_command()

    def __parse_next_command(self):
        if Command.is_compress_command(self.__bytes[self.__index]):
            command = CommandCompress(self.__get_next_block('compress'))
        else:
            command = CommandUncompress(self.__get_next_block('compress'))


class Command:
    def __init__(self, bits):
        self.__bits = bits

    @staticmethod
    def is_compress_command(byte):
        bits = bin(int(byte, 16))[2:]
        if bits[::-1][:2] == '11':
            return False
        return True


class CommandCompress(Command):
    pass


class CommandUncompress(Command):
    pass

from pprint import pprint

from . import format
from .exceptions import *
from .elf_obj import Elf32, CommandsBase


def normalize_bytes(_bytes):
    hex_string = '0x'
    for byte in _bytes[::-1]:
        hex_string += '0' if len(hex(int(byte, 16))) < 4 else ''
        hex_string += byte[2:]
    return hex_string


def bytes_to_string(_bytes):
    return ''.join([chr(int(i, 16)) for i in _bytes])


def matcher(_bytes, match, normalize=True):
    out = []
    for indexes, name in match.items():
        if normalize:
            value = normalize_bytes(_bytes[indexes[0]: indexes[1]])
            value = hex(int(value, 16))
        else:
            value = _bytes[indexes[0]: indexes[1]]
        out.append((name, value))
    return out


@check_elf_reader_exception
def read(path):
    with open(path, 'rb') as elf_file:
        _bytes = elf_file.read()
        _bytes = [hex(byte) for byte in _bytes]

    elf = Elf32()
    header = parse_header(_bytes)
    elf.add_headers(header)
    sections = parse_sections(_bytes[elf.E_SHOFF:], elf.E_SHNUM)
    elf.add_sections(sections)

    # get offset for section with name
    section_keep_names = sections[elf.E_SHSTRNDX]
    sections_names_offsets = [int(i[0][1], 16) for i in sections]
    sections_names = parse_section_name(_bytes[int(dict(section_keep_names)["SH_OFFSET"], 16):], sections_names_offsets)
    elf.add_names(sections_names)

    section_symtab = elf.get_section_by_name('.symtab')
    symtab_table = parse_symtab(_bytes[int(section_symtab["SH_OFFSET"], 16):], int(section_symtab["SH_SIZE"], 16) // 16)
    section_strtab = elf.get_section_by_name('.strtab')
    sections_names_offsets = [int(i[0][1], 16) for i in symtab_table]
    strtab_table = parse_section_name(_bytes[int(dict(section_strtab)["SH_OFFSET"], 16):], sections_names_offsets)
    for i in range(len(symtab_table)):
        symtab_table[i].append(("PARSE_NAME", strtab_table[i]))
    elf.add_symtab(symtab_table)
    # print(elf.get_string_symtab())

    text_section = elf.get_section_by_name('.text')
    text_section_start_ind = int(dict(text_section)['SH_OFFSET'], 16)
    text_section_size = int(dict(text_section)['SH_SIZE'], 16)
    # pprint(text_section)
    _bytes_text = _bytes[text_section_start_ind: text_section_start_ind + text_section_size]
    commands = CommandsBase(_bytes_text)
    # commands = parse_text(_bytes_text)
    # for i in range(4):
    #     print(hex(_bytes[i*32: (i+1)*32]))


def parse_header(_bytes):
    e_ident = list(zip(format.math_e_ident.keys(), _bytes[:16]))

    # next only for 32
    header = matcher(_bytes, format.match_header) + e_ident
    check_header(dict(header))

    return header


def check_header(header: dict):
    for name, accept_value in \
            (format.match_header_white_list | format.math_e_ident).items():
        if accept_value and int(header[name], 16) not in accept_value:
            raise Incorrect_Data(name, header[name])

        # kludge
        if name == 'E_SHENTSIZE':
            if int(header[name], 16) != 0x28:
                raise


def parse_sections(_bytes, E_SHNUM):
    sections = []
    for i in range(E_SHNUM):
        sections.append(matcher(_bytes[40 * i:], format.match_section))
    return sections


def parse_section_name(_bytes, offsets):
    names = []
    for off in offsets:
        current_index = off
        while int(_bytes[current_index], 16) != 0x0:
            current_index += 1
        names.append(bytes_to_string(_bytes[off: current_index]))
    return names


def parse_symtab(_bytes, count):
    symtabs = []
    for i in range(count):
        symtabs.append(matcher(_bytes[16 * i:], format.match_symtab))
    return symtabs


def parse_text(_bytes):
    commands = []
    index = 0
    while index < len(_bytes):
        if is_compress_command(_bytes[index]):
            commands.append(parse_compress_command(_bytes[index: index + 2]))
            index += 2
        else:
            commands.append(parse_uncompress_command(_bytes[index: index + 4]))
            index += 4


def is_compress_command(byte):
    bits = bin(int(byte, 16))[2:]
    if bits[::-1][:2] == '11':
        return False
    return True


def parse_compress_command(_bytes):
    return '1'


def parse_uncompress_command(_bytes):
    bits = ''.join([bin(int(i, 16))[2:].rjust(8, '0') for i in _bytes[::-1]])

    name, _type = get_name_type(bits)

    attr = matcher(bits[::-1], format.match_uncompress_command[_type], normalize = False)
    values = {}
    for i in attr:
        values[i[0]] = i[1][::-1]

    if _type == 'R':
        # print(values['rd'], values['rs1'], values['rs2'])
        print(int(values['rd'], 2), int(values['rs1'], 2), int(values['rs2'], 2))

    # print(bits, name, _type)


def get_command_type(bits):
    opcode = bits[-7:]
    for row in format.base_uncompress:
        if row['opcode'] == opcode:
            name = row['name']
            funct7 = ''
            funct3 = ''
            if 'funct7' in row:
                funct7 = bits[-32: -25]
            if 'funct3' in row:
                funct3 = bits[-15: -12]

            if funct3 or funct7:
                for row2 in format.base_uncompress:

                    if funct7:
                        if row2['opcode'] == opcode and \
                                (row2['funct3'] == funct3) and \
                                (row2['funct7'] == funct7):
                            name = row['name']
                            break
                    else:
                        if row2['opcode'] == opcode and \
                                (row2['funct3'] == funct3):
                            name = row['name']
                            break

                else:
                    print('error', bits, funct3, funct7)
                    raise

            _type = row['type']
            break
    else:
        print('error')
        raise
    return name, _type



# def parse_symtab_names(_bytes, offsets):
#     names = []
#     for off in offsets:
#         current_index = off
#         while int(_bytes[current_index], 16) != 0x0:
#             current_index += 1
#         names.append(bytes_to_string(_bytes[off: current_index]))
#     return names

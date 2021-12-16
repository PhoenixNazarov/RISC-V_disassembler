from pprint import pprint

import settings as st
from elf_parser import config as fm
from elf_parser.exceptions import *
from elf_parser.elf_obj import Elf32, CommandsBase, Command


def normalize_bytes(_bytes):
    hex_string = '0x'
    for byte in _bytes[::-1]:
        hex_string += '0' if len(hex(int(byte, 16))) < 4 else ''
        hex_string += byte[2:]
    return hex_string


def bytes_to_string(_bytes):
    return ''.join([chr(int(i, 16)) for i in _bytes])


def matcher(_bytes, match):
    out = []
    for indexes, name in match.items():
        value = normalize_bytes(_bytes[indexes[0]: indexes[1]])
        value = hex(int(value, 16))
        out.append((name, value))
    return out


@check_elf_reader_exception
def read(data, _type='from_file') -> Elf32:
    if _type == 'from_file':
        with open(data, 'rb') as elf_file:
            _bytes = elf_file.read()
            _bytes = [hex(byte) for byte in _bytes]
    elif _type == 'from_bytes':
        _bytes = [hex(byte) for byte in data]
    else:
        raise "Incorrect value"

    # Parse Header
    elf = Elf32()
    header = parse_header(_bytes)
    elf.set_headers(header)

    # Parse Sections
    sections = parse_sections(_bytes[elf.get_var('E_SHOFF', 'headers'):], elf.get_var('E_SHNUM', 'headers'))
    section_keep_names = sections[elf.get_var('E_SHSTRNDX', 'headers')]
    sections_names_offsets = [int(i[0][1], 16) for i in sections]
    sections_names = parse_section_name(_bytes[int(dict(section_keep_names)["SH_OFFSET"], 16):], sections_names_offsets)
    elf.set_sections(sections, sections_names)

    # Parse Symtab
    section_symtab = elf.get_section_by_name('.symtab')
    symtab_table = parse_symtab(_bytes[int(section_symtab["SH_OFFSET"], 16):], int(section_symtab["SH_SIZE"], 16) // 16)
    section_strtab = elf.get_section_by_name('.strtab')
    sections_names_offsets = [int(i[0][1], 16) for i in symtab_table]
    strtab_table = parse_section_name(_bytes[int(section_strtab["SH_OFFSET"], 16):], sections_names_offsets)
    for i in range(len(symtab_table)):
        symtab_table[i].append(("PARSE_NAME", strtab_table[i]))
    elf.add_symtab(symtab_table)

    # Parse Text
    name_table = st.name_section_of_riscv
    text_section = elf.get_section_by_name(name_table)
    text_section_start_ind = int(text_section['SH_OFFSET'], 16)
    text_section_size = int(text_section['SH_SIZE'], 16)

    _bytes_text = _bytes[text_section_start_ind: text_section_start_ind + text_section_size]
    commands = CommandsBase(_bytes_text, int(text_section['SH_ADDR'], 16))
    elf.add_command(commands)
    return elf


def parse_header(_bytes):
    e_ident = list(zip(fm.match_e_ident.keys(), _bytes[:16]))

    # next only for 32
    header = matcher(_bytes, fm.match_header) + e_ident
    check_header(dict(header))

    return header


def check_header(header: dict):
    for name, accept_value in \
            (fm.match_header_white_list | fm.match_e_ident).items():
        if accept_value and int(header[name], 16) not in accept_value:
            raise Incorrect_Data(name, header[name])

        # kludge
        if name == 'E_SHENTSIZE':
            if int(header[name], 16) != 0x28:
                raise


def parse_sections(_bytes, E_SHNUM):
    sections = []
    for i in range(E_SHNUM):
        sections.append(matcher(_bytes[40 * i:], fm.match_section))
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
        symtabs.append(matcher(_bytes[16 * i:], fm.match_symtab))
    return symtabs

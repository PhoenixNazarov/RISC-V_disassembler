from elf_parser.reader import read

import sys

# Out formats
symtab_name = "{numb} {value:15} {size:>5} {type:8} {bind:8} {vis:8} {index:>6} {name}\n"
symtab_data = "[{numb:>4}] {value:15} {size:>5} {type:8} {bind:8} {vis:8} {index:>6} {name}\n"
command_data = "{:08x} {:10}: {} {}\n"

def main(input_path, output_path):
    # to inspect
    from elf_parser.elf_obj import Elf32
    elf: Elf32

    with open(input_path, 'rb') as elf_file:
        _bytes = elf_file.read()

    elf = read(_bytes, _type = 'from_bytes')

    elf.set_format('symtab_name', symtab_name)
    elf.set_format('symtab_data', symtab_data)
    elf.set_format('commands', command_data)

    # out = elf.to_string(param = 'header')
    # out = elf.to_string(param = 'sections')
    # out = elf.to_string(param = 'symtab')
    # out = elf.to_string(param = 'commands')
    out = elf.to_string(param = 'to_test')
    # print(out)

    with open(output_path, 'w') as file:
        file.write(out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])


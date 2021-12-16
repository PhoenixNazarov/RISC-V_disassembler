from elf_parser.reader import read
import sys


def main(input_path, output_path):
    with open(input_path, 'rb') as elf_file:
        _bytes = elf_file.read()
    elf = read(_bytes, _type = 'from_bytes')

    # out = elf.to_string(param = 'header')
    # out = elf.to_string(param = 'sections')
    # out = elf.to_string(param = 'symtab')
    # out = elf.to_string(param = 'commands')
    out = elf.to_string(param = 'to_test')

    with open(output_path, 'w') as file:
        file.write(out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])


import elf_parser


def main(path_elf):
    elf = elf_parser.read(path_elf)


if __name__ == '__main__':
    main('test.elf')


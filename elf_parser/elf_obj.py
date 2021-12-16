from pprint import pformat

from elf_parser import config as fm
import settings as st


class Elf32:
    def __init__(self):
        self.__headers = {}
        self.__sections = []
        self.__sections_names = []
        self.__symtab = []
        self.__commandsBase = None

    def get_var(self, name, place, form_out='int16'):
        out = ''
        if place == 'headers':
            out = dict(self.__headers)[name]

        if out == '':
            raise ValueError

        match form_out:
            case "int16":
                return int(out, 16)

    def set_headers(self, headers):
        self.__headers = headers

    def set_sections(self, sections, names):
        self.__sections = sections
        self.__sections_names = names

    def add_symtab(self, symtab):
        self.__symtab += symtab
        self.get_symtab_for_command()

    def add_command(self, commandsBase):
        self.__commandsBase = commandsBase

    def get_symtab_for_command(self):
        out = {}
        for i in self.__symtab:
            for ii in i:
                if ii[0] == 'VALUE':
                    val = int(ii[1], 16)
                if ii[0] == 'PARSE_NAME':
                    name = ii[1]
            out.update({val: {'name': name}})
        Command.symtab = out

    def get_section_by_name(self, name):
        # if name in '.symtab':
        for i in range(len(self.__sections_names)):
            if name == self.__sections_names[i]:
                return dict(self.__sections[i])

    def __symtab_to_string(self):
        index = 0
        string = st.symtab_name
        in_format = [
            lambda SIZE: int(SIZE, 16),
            lambda INFO: fm.symtab_types[int(INFO, 16) & 15],
            lambda INFO: fm.symtab_binds[int(INFO, 16) >> 4],
            lambda OTHER: fm.symtab_vises[int(OTHER, 16 & 3)],
            # next need pre int(SHNDX, 16)
            lambda SHNDX: fm.symtab_special[SHNDX] if SHNDX in fm.symtab_special.keys() else SHNDX,
        ]
        for _row in self.__symtab:
            row = dict(_row)
            string += st.symtab_data.format(
                numb = index,
                value = row["VALUE"],
                size = in_format[0](row["SIZE"]),
                type = in_format[1](row["INFO"]),
                bind = in_format[2](row['INFO']),
                vis = in_format[3](row['OTHER']),
                index = in_format[4](int(row['SHNDX'], 16)),
                name = row["PARSE_NAME"])
            index += 1
        return string

    def __commands_to_string(self):
        return self.__commandsBase.to_string(st.command_data)

    def __sections_to_string(self):
        string = ''
        index = 0
        for i in self.__sections:
            string += pformat([('name', self.__sections_names[index])] + i)
            string += '\n\n'
            index += 1
        return string

    def to_string(self, param):
        match param:
            case "symtab":
                return '.symtab\n' + self.__symtab_to_string()
            case "commands":
                return st.name_section_of_riscv+'\n' + self.__commands_to_string()
            case "to_test":
                out = st.name_section_of_riscv + '\n'
                out += self.__commands_to_string()
                out += '\n'
                out += '.symtab\n'
                out += self.__symtab_to_string()
                return out
            case "header":
                return pformat(self.__headers)
            case "sections":
                return self.__sections_to_string()


class CommandsBase:
    def __init__(self, _bytes, first_address):
        self.__bytes = _bytes
        self.__first_addr = first_address
        self.__commands = []
        self.__index = 0
        self.__parse_commands()

    def __get_next_block(self, _type):
        if _type == 'compress':
            out = self.__bytes[self.__index: self.__index + 2]
            self.__index += 2
        else:
            out = self.__bytes[self.__index: self.__index + 4]
            self.__index += 4
        return out

    def __parse_commands(self):
        while self.__index < len(self.__bytes):
            self.__parse_next_command()

    def __parse_next_command(self):
        cur_addr = self.__first_addr + self.__index
        if Command.is_compress_command(self.__bytes[self.__index]):
            command = CommandCompress(self.__get_next_block('compress'), cur_addr)
        else:
            command = CommandUncompress(self.__get_next_block('uncompress'), cur_addr)
        self.__commands.append(command)

    def to_string(self, _format):
        for i in self.__commands:
            i.collect_data()
        for i in self.__commands:
            i.update_points()

        string = ''
        for i in self.__commands:
            string += _format.format(
                *i.take_var_to_format()
            )

        return string


class Command:
    _points = {}
    symtab = {}
    cur_point = 0

    def __init__(self, _bytes, addr):
        self._bits = self.bytes_to_bites(_bytes)
        self.addr = addr
        self.string = ''
        self.start = ''
        self.end = ''
        self.scenario()

    def take_var_to_format(self):
        return [
            self.addr,
            self.start,
            self.string,
            self.end
        ]

    @staticmethod
    def bytes_to_bites(_bytes):
        return ''.join([bin(int(i, 16))[2:].rjust(8, '0') for i in _bytes[::-1]])

    @staticmethod
    def is_compress_command(byte):
        bits = bin(int(byte, 16))[2:]
        if bits[::-1][:2] == '11':
            return False
        return True

    @staticmethod
    def matcher(_bites, match):
        out = []
        for indexes, name in match.items():
            value = _bites[indexes[0]: indexes[1]]
            out.append((name, value))
        return out

    @staticmethod
    def register_by_ABI(rd):
        if type(rd) == type(''):
            rd = int(rd, 2)
        for indexes, value in fm.ABI_REGISTERS.items():
            if indexes[0] <= rd < indexes[1]:
                if type(value) == type(lambda: 1):
                    return value(rd)
                elif type(value) == type(''):
                    return value
                else:
                    raise "Внутренняя ошибка"
        return 'unknown_abi'

    @staticmethod
    def register_for_csr(csr):
        # for p1, p2 in fm.csr_alot_registers.keys():
        #     print(p1, int(csr, 2), p2)
        #     if p1 <= int(csr, 2) <= p2:
        #         print('ok')
        is_alot =  [p1 <= int(csr, 2) <= p2 for p1, p2 in fm.csr_alot_registers.keys()]
        if any(is_alot):
            return list(fm.csr_alot_registers.values())[is_alot.index(1)]
        if f"0x{(int(csr, 2)):03x}" in fm.csr_registers:
            return fm.csr_registers[f"0x{(int(csr, 2)):03x}"]
        print(csr)
        return 'unknown_csr'

    @staticmethod
    def additional_to_2(bits: str):
        if bits[0] == '0':
            return int(bits, 2)
        return -int(''.join(map(str, [int((not int(i))) for i in bits[1:]])), 2) - 1

    def update_points(self):
        if self.addr in self._points:
            self.start = f'{self._points.pop(self.addr)["name"]}  '
        if self.addr in self.symtab:
            self.start += f'{self.symtab.pop(self.addr)["name"]}  '

    def jump(self, offset):
        addr_point = self.addr + offset
        if addr_point in self.symtab:
            self.end = self.symtab[addr_point]['name']
        else:
            match st.new_lock_name_type:
                case 'addr':
                    loc_name = f'LOC_{addr_point:05x}'
                case 'count':
                    loc_name = f'LOC_{self.cur_point:05x}'
                    self.cur_point += 1
                case _: raise "new_lock_name_type in settings.py set incorrect"

            self.end = loc_name
            self._points.update({addr_point: {'name': loc_name}})

        match st.branch_jump_out_type:
            case 'addr_hex':
                return f'{addr_point:08x}'
            case 'offset_dec':
                return f'{offset}'
            case 'addr_dec':
                return f'{addr_point}'
            case _:
                raise 'branch_jump_out_type in settings.py set incorrect'

    def frm(self, _type, *args):
        match _type:
            case "b_j":
                if st.branch_jump_out_type == 'addr_hex':
                    return f'{args[0]:08x}'
                elif st.branch_jump_out_type == 'offset_dec':
                    return f'{args[1]}'
                elif st.branch_jump_out_type == 'addr_dec':
                    return f'{args[0]}'
                else:
                    raise 'branch_jump_type_out in settings.py set incorrect'


    def scenario(self):
        raise "Эта функция должна быть переопределена"

    def collect_data(self):
        raise "Эта функция должна быть переопределена"


class CommandCompress(Command):
    def scenario(self):
        self.__name = ''
        self.__first_code = ''

        self.__get_name()

    def __get_name(self):
        self.__first_code = self._bits[-2:]
        second_code = self._bits[:3]

        if self._bits == '0' * 16:
            self.__name = 'unimp'
        elif (self.__first_code, second_code) in fm.compress_names:
            self.__name = fm.compress_names[(self.__first_code, second_code)]

    def collect_data(self):
        if self.__name in ['unimp']:
            self.string = 'unimp'
            return

        match self.__first_code:
            case '00':
                rd = fm.match_compress['r42']
                rs1 = fm.match_compress['r97']
                if self.__name == 'addi4spn':
                    self.string = f'{self.__name}'


class CommandUncompress(Command):
    def scenario(self):
        self.__opcode = self._bits[-7:]
        self.__type = ''
        self.__values = {}
        self.__name = ''

        self.__get_type()
        if self.__type == -1:
            return
        self.__match_data()
        self.__get_name()

    def __get_type(self):
        match self.__opcode:
            case fm.RI_conflict:
                funct3 = self._bits[::-1][12: 15][::-1]
                if funct3 in fm.funct3_R:
                    self.__type = 'R'
                else:
                    self.__type = 'I'

            case fm.e_opcode:
                funct3 = self._bits[::-1][12: 15][::-1]
                if funct3 == '000':
                    self.__type = 'I'
                else:
                    self.__type = 'I'

            case _:
                find = 0
                for type_name, opcodes in fm.opcodes_type.items():
                    if self.__opcode in opcodes:
                        find += 1
                        self.__type = type_name
                # print(self.__opcode)
                if self.__opcode == '1110011':
                    print(find)

                if find != 1:
                    self.__type = -1
                    # raise "Не удалось определить type для команды " + self.__opcode

    def __match_data(self):
        format_parse = fm.match_uncompress_command[self.__type]
        attr = self.matcher(self._bits[::-1], format_parse)
        for i in attr:
            self.__values.update({i[0]: i[1][::-1]})

    def collect_data(self):
        if self.__opcode == fm.csr_opcode:
            funct3 = self.__values['funct3']
            rd = self.register_by_ABI(self.__values['rd'])
            rs1 = self.register_by_ABI(self.__values['rs1'])
            csr = self.register_for_csr(self.__values["imm11"])
            self.string = f'{self.__name} {rd}, {csr}, {rs1}'
            if self._bits == '0' * 32:
                self.string = st.rvc_illegal_instruction
            # match funct3:
            #     case '010':
            #         self.string = f'{self.__name} {rd}, {csr}'
            #     case _:
            #         self.string = f'{self.__name} {rd}, {rs1}, {csr}'
            return
        match self.__type:
            case "R":
                rd = self.register_by_ABI(self.__values['rd'])
                rs1 = self.register_by_ABI(self.__values['rs1'])
                rs2 = self.register_by_ABI(self.__values['rs2'])
                if self.__name in fm.R_type_except:
                    rs2 = hex(int(self.__values['rs2'], 2))
                    self.string = f'{self.__name} {rd}, {rs1}, {rs2}'
                else:
                    self.string = f'{self.__name} {rd}, {rs1}, {rs2}'

            case "I":
                rd = self.register_by_ABI(self.__values['rd'])
                rs1 = self.register_by_ABI(self.__values['rs1'])
                imm = self.additional_to_2(fm.IMMS_UMCOMPRESS['I'](self.__values["imm11"]))  # imm[11:0]
                if self._bits == fm.nop and st.nop:
                    self.string = 'nop'
                elif self.__name in fm.I_type_except:
                    self.string = f'{self.__name} {rd}, {imm}({rs1})'
                elif self.__name in fm.I_control:
                    self.string = f'{self.__name}'
                else:
                    self.string = f'{self.__name} {rd}, {rs1}, {imm}'

            case "S":
                rs1 = self.register_by_ABI(self.__values['rs1'])
                rs2 = self.register_by_ABI(self.__values['rs2'])
                imm115 = self.__values['imm115']  # imm[11:5]
                imm4 = self.__values['imm4']  # imm[4:0]
                imm = self.additional_to_2(fm.IMMS_UMCOMPRESS['S'](imm115, imm4))
                self.string = f'{self.__name} {rs2}, {imm}({rs1})'

            case "B":
                rs1 = self.register_by_ABI(self.__values['rs1'])
                rs2 = self.register_by_ABI(self.__values['rs2'])
                imm12105 = self.__values['imm12105']  # imm[12|10:5]
                imm4111 = self.__values['imm4111']  # imm[4:1|11]
                imm = self.additional_to_2(fm.IMMS_UMCOMPRESS['B'](imm12105, imm4111))

                # addr_point = self.addr + imm
                # if addr_point in self.symtab:
                #     print('b_in')
                #     self.end = self.symtab[addr_point]['name']
                # else:
                #     print('b_else')
                #     self.end = f'LOC_{addr_point:05x}'

                self.string = f'{self.__name} {rs1}, {rs2}, {self.jump(imm)}'

            case "U":
                rd = self.register_by_ABI(self.__values['rd'])
                imm = self.additional_to_2(fm.IMMS_UMCOMPRESS['U'](self.__values['imm3112']))
                if not st.u_imm_dec_type:
                    imm = hex(imm)

                self.string = f'{self.__name} {rd}, {imm}'

            case "J":
                rd = self.register_by_ABI(self.__values['rd'])
                imm = self.additional_to_2(fm.IMMS_UMCOMPRESS['J'](self.__values['imm2010']))
                # addr_point = self.addr + imm
                #
                # if addr_point in self.symtab:
                #     print('j in')
                #     self.end = self.symtab[addr_point]['name']
                # else:
                #     print('j else')
                #     self.end = f'LOC_{addr_point:05x}'
                #     self._points.update({addr_point: ''})
                self.string = f'{self.__name} {rd}, {self.jump(imm)}'

            case _:
                self.string = 'unknown_command'

        return self.string

    def __get_name(self):
        suitable_rows = []
        for row in fm.base_uncompress:
            if row['opcode'] == self.__opcode:
                suitable_rows.append(row)

        if len(suitable_rows) == 0:
            raise 'Необрабатываемая команда'

        if len(suitable_rows) == 1:
            self.__name = suitable_rows[0]['name']
            return

        for row in suitable_rows:
            match self.__values:
                case {'funct3': funct3, "funct7": funct7}:
                    if funct3 == row['funct3'] and funct7 == row['funct7']:
                        self.__name = row['name']
                        break
                case {'funct3': funct3}:
                    if funct3 == row['funct3']:
                        self.__name = row['name']
                        break
        else:
            print(self.__type, self.__values)
            raise 'Не удалось найти функцию'

    def __str__(self):
        # DEBUG
        match self.__type:
            # case "R":
            #     return self.string
            # case "I":
            #     return self.string
            case "S":
                return self.string
            case _:
                return f"undef"

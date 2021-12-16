from pprint import pformat
from functools import wraps

from elf_parser.exceptions import *
from elf_parser import config as fm
import settings as st


@check_global_funct
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
            print(f'{name} {place} the program could not find the specified parameters')
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
            val, name, _type = None, None, None
            for ii in i:
                if ii[0] == 'VALUE':
                    val = int(ii[1], 16)
                if ii[0] == 'PARSE_NAME':
                    name = ii[1]
                if ii[0] == 'INFO':
                    _type = fm.symtab_types[int(ii[1], 16) & 15]

            if val is None or name is None:
                print('one row in symtab is broken')
                continue

            if val in out and _type != 'FUNC':
                continue
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
                return st.name_section_of_riscv + '\n' + self.__commands_to_string()
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
        _error = [0]
        row = 0

        def checker(func):
            try:
                return func()
            except Exception as e:
                print(e)
                _error[0] += 1
                return None

        for i in self.__commands:
            checker(i.collect_data)
        for i in self.__commands:
            checker(i.update_points)

        string = ''
        for i in self.__commands:
            row += 1
            values = checker(i.take_var_to_format)
            if values is None:
                string += 'exception on this row\n'
                continue
            string += _format.format(*values)

        print(f'complete parse command with {_error[0]}/{row} errors')
        return string


class Command:
    _points = {}
    symtab = {}
    cur_point = [-1]

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
    @replace_unknown_data('0' * 32)
    def matcher(_bites, match):
        out = []
        for indexes, name in match.items():
            value = _bites[indexes[0]: indexes[1]]
            out.append((name, value))
        return out

    @staticmethod
    @replace_unknown_data('unknown_abi')
    def register_by_ABI(rd, compress=False):
        if compress:
            if rd in fm.ABI_REGISTERS_compress:
                return fm.ABI_REGISTERS_compress[rd]
            return 'unknown_copmpress_abi_' + rd
        if type(rd) == type(''):
            rd = int(rd, 2)

        for indexes, value in fm.ABI_REGISTERS.items():
            if indexes[0] <= rd < indexes[1]:
                if type(value) == type(lambda: 1):
                    return value(rd)
                elif type(value) == type(''):
                    return value
        return 'unknown_abi'

    @staticmethod
    @replace_unknown_data('unknown_csr')
    def register_for_csr(csr):
        is_alot = [p1 <= int(csr, 2) <= p2 for p1, p2 in fm.csr_alot_registers.keys()]
        if any(is_alot):
            return list(fm.csr_alot_registers.values())[is_alot.index(1)]
        if f"0x{(int(csr, 2)):03x}" in fm.csr_registers:
            return fm.csr_registers[f"0x{(int(csr, 2)):03x}"]
        return 'unknown_csr'

    @staticmethod
    def additional_to_2(bits: str):
        if bits[0] == '0':
            return int(bits, 2)
        return -int(''.join(map(str, [int((not int(i))) for i in bits[1:]])), 2) - 1

    def cal_with_settings(self, name, val):
        match name, fm.settings[name]:
            case 'U_NOTION' | "BJ_NOTION", 'hex':
                return f'0x{int(val, 2):x}'
            case 'U_NOTION' | "BJ_NOTION", 'dec':
                if type(val) != int:
                    return self.additional_to_2(val)
                return val
            case 'SSS_NOTION', 'hex':
                return hex(int(val, 2))
            case 'SSS_NOTION', 'dec':
                if type(val) != int:
                    return int(val, 2)
                return val

            case "BJ_VAL", "addr":
                return self.cal_with_settings("BJ_NOTION", self.addr + val)
            case "BJ_VAL", "offset":
                return self.cal_with_settings("BJ_NOTION", val)

            case "LOC_VAL", 'addr':
                return f'LOC_{val:05x}'
            case "LOC_VAL", 'count':
                self.cur_point[0] += 1
                return f'LOC_{self.cur_point[0]:05x}'

            case _:
                raise "new_lock_name_type in settings.py set incorrect"

    def update_points(self):
        if self.addr in self._points:
            self.start = f'{self._points.pop(self.addr)["name"]}:  '
        if self.addr in self.symtab:
            self.start += f'{self.symtab.pop(self.addr)["name"]}:  '

    def jump(self, offset):
        addr_point = self.addr + offset
        if addr_point in self.symtab:
            self.end = self.symtab[addr_point]['name']
        else:
            loc_name = self.cal_with_settings("LOC_VAL", addr_point)
            self.end = loc_name
            self._points.update({addr_point: {'name': loc_name}})

        return self.cal_with_settings("BJ_VAL", offset)

    def scenario(self):
        raise "This function needs to be overridden"

    def collect_data(self):
        raise "This function needs to be overridden"


class CommandCompress(Command):
    def scenario(self):
        self.__name = ''
        self.__first_code = ''
        self.__values = {}

        self.__get_name()
        self.__match_data()

    @replace_unknown_data('unknown_name')
    def __get_name(self):
        self.__first_code = self._bits[-2:]
        second_code = self._bits[:3]

        if self._bits == '0' * 16:
            self.__name = st.rvc_illegal_instruction
            return

        elif (self.__first_code, second_code) in fm.compress_names:
            self.__name = fm.compress_names[(self.__first_code, second_code)]

    def __get_match_block(self, v):
        for i in fm.rvc_blocks:
            if v in i:
                return fm.rvc_match['r'](self._bits, fm.rvc_blocks[i][0], fm.rvc_blocks[i][1])
        else:
            raise v

    def __match_data(self):
        if self.__name == 'lui/addi16sp':
            if int(fm.rvc_match['r'](self._bits, 11, 7), 2) == 2:
                self.__name = 'addi16sp'
            else:
                self.__name = 'lui'

        for cmd in fm.rvcsss:
            if cmd == self.__name:
                f_vars = fm.rvcsss[cmd]
                break
        else:
            return

        for v in f_vars:
            if v.startswith('block'):
                val = f_vars[v](self.__get_match_block(v))
            elif type(f_vars[v]) == type(''):
                bloc_pos = self.__get_match_block(f_vars[v])
                val = fm.rvc_match[f_vars[v]](bloc_pos)
            else:
                val = f_vars[v](self._bits)
            self.__values.update({v: val})

    def collect_data(self):
        # ABI
        for i in self.__values:
            if i.startswith('r'):
                self.__values[i] = self.register_by_ABI(self.__values[i], compress = True)
            elif i.startswith('_r'):
                if self.__name == 'lwsp':
                    if int(self.__values[i], 2) == '0':
                        self.__name = st.unknown_rvc
                        break
                self.__values[i] = self.register_by_ABI(self.__values[i])

        match self.__name:
            case st.rvc_illegal_instruction:
                pass
            case "addi4spn":
                nzuimm = int((self.__values["nzuimm"]), 2) * 4
                self.string = f'{self.__values["rd"]}, sp, {nzuimm}'
            case "lw" | "sw" as nm:
                sp = self.__values["rs1"]
                if nm == 'lw':
                    fp = self.__values["rd"]
                else:
                    fp = self.__values["rs2"]
                imm = self.additional_to_2(self.__values["uimm5326"])
                self.string = f'{fp}, {imm}({sp})'
            case "addi":
                imm = int(self.__values["nzimm540"], 2)
                if imm == 0:
                    self.__name = 'nop'
                else:
                    self.string = f'{self.__values["_r"]}, {self.__values["_r"]}, {imm}'
            case "li":
                imm = self.additional_to_2(self.__values["imm"])
                self.string = f'{self.__values["_rd"]}, {imm}'
            case "lui":
                imm = int(self.__values["nzimm"], 2)
                self.string = f'{self.__values["_rd"]}, {imm}'
            case "addi16sp":
                nzuimm = int(self.__values["block_nzimm9--4-6-8-7-5"], 2) * 16
                self.string = f'{self.__values["_rd"]}, sp, {nzuimm}'
            case "j":
                block_imm = self.additional_to_2(self.__values["block_imm"])
                self.string = f'{self.jump(block_imm)}'
            case "beqz" | "bnez":
                block_imm = self.additional_to_2(self.__values["imm"])
                self.string = f'{self.__values["rs1"]}, {self.jump(block_imm)}'
            case "slli":
                imm = hex(int(self.__values["nzuim"], 2))
                self.string = f'{self.__values["_r"]}, {imm}'
            case "lwsp":
                imm = int(self.__values['uimm'], 2)
                self.string = f'{self.__values["_rd"]}, {imm}(sp)'
            case "swsp":
                imm = int(self.__values['uimm'], 2)
                self.string = f'{self.__values["_rs2"]}, {imm}(sp)'
            case "j[al]r/mv/add":
                match self.__values['code1'], self.__values['code2'], self.__values['code3']:
                    case '0' | '1' as c1, rs1, '00000':
                        if c1 == '0':
                            self.__name = 'jr'
                        else:
                            self.__name = 'jalr'
                        self.string = f'{self.register_by_ABI(rs1)}'
                    case '0', rd, rs2:
                        self.__name = 'mv'
                        self.string = f'{self.register_by_ABI(rd)} {self.register_by_ABI(rs2)}'
                    case '1', '00000', '00000':
                        self.__name = 'ebreak'
                    case '1', r, rs2:
                        self.__name = 'add'
                        r = self.register_by_ABI(r)
                        self.string = f'{r}, {r}, {self.register_by_ABI(rs2)}'
                    case _:
                        self.__name = st.unknown_rvc
            case "misc-alu":
                sv = self.__values
                match sv['rs'], sv['code1'], sv['code2'], sv['code3'], sv['rs2'], sv['imm']:
                    case rs, '0', '11', '00' | '01' | '10' | '11' as cd, rs2, _:
                        self.__name = ['sub', 'xor', 'or', 'and'][int(cd, 2)]
                        self.string = f'{rs}, {rs}, {rs2}'

                    case rs, im5, '10', _, _, im4:
                        self.__name = 'andi'
                        self.string = f'{rs}, {rs}, {self.additional_to_2(im5 + im4)}'
                    case _:
                        self.__name = st.unknown_rvc
            case _:
                self.__name = st.unknown_rvc

        self.string = st.rvc_prefix + f'{self.__name} ' + self.string


class CommandUncompress(Command):
    def scenario(self):
        self.__opcode = self._bits[-7:]
        self.__type = ''
        self.__values = {}
        self.__name = ''

        self.__type = self.__get_type()
        if self.__type == -1:
            return
        self.__match_data()
        self.__get_name()

    @replace_unknown_data('unknown_type')
    def __get_type(self):
        match self.__opcode:
            case fm.RI_conflict:
                funct3 = self._bits[::-1][12: 15][::-1]
                if funct3 in fm.funct3_R:
                    return 'R'
                else:
                    return 'I'

            case fm.e_opcode:
                funct3 = self._bits[::-1][12: 15][::-1]
                if funct3 == '000':
                    return 'I'
                else:
                    return 'I'

            case _:
                find = 0
                for type_name, opcodes in fm.opcodes_type.items():
                    if self.__opcode in opcodes:
                        find += 1
                        return type_name

                if find != 1:
                    return -1

    def __match_data(self):
        format_parse = fm.match_uncompress_command[self.__type]
        attr = self.matcher(self._bits[::-1], format_parse)
        for i in attr:
            self.__values.update({i[0]: i[1][::-1]})

    def collect_data(self):
        if self.__name.startswith('csr'):
            rd = self.register_by_ABI(self.__values['rd'])
            csr = self.register_for_csr(self.__values["imm11"])
            if self.__name.endswith('i'):
                uimm = self.additional_to_2(self.__values['rs1'])
                self.string = f'{self.__name} {rd}, {csr}, {uimm}'
            else:
                rs1 = self.register_by_ABI(self.__values['rs1'])
                self.string = f'{self.__name} {rd}, {csr}, {rs1}'
            return

        match self.__type:
            case "R":
                rd = self.register_by_ABI(self.__values['rd'])
                rs1 = self.register_by_ABI(self.__values['rs1'])
                rs2 = self.register_by_ABI(self.__values['rs2'])
                if self.__name in fm.R_type_except:
                    rs2 = self.cal_with_settings("SSS_NOTION", self.__values['rs2'])
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
                    if self.__opcode == '0001111':
                        self.string = f'fence'
                    elif self._bits.startswith('00000000000000'):
                        self.string = f'{self.__name}'
                    else:
                        self.string = f'ecall'
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
                self.string = f'{self.__name} {rs1}, {rs2}, {self.jump(imm)}'

            case "U":
                rd = self.register_by_ABI(self.__values['rd'])
                imm = fm.IMMS_UMCOMPRESS['U'](self.__values['imm3112'])
                imm = self.cal_with_settings('U_NOTION', imm)
                self.string = f'{self.__name} {rd}, {imm}'

            case "J":
                rd = self.register_by_ABI(self.__values['rd'])
                imm = self.additional_to_2(fm.IMMS_UMCOMPRESS['J'](self.__values['imm2010']))
                self.string = f'{self.__name} {rd}, {self.jump(imm)}'

            case _:
                self.string = st.unknown

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

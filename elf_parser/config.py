# This file contains information about structure elf's file
# match_* - List with "Index markup" for work with function reader.matcher()
# *_white_list - List with true data


# HEADER
match_e_ident = {
    "EI_MAG0": [0x7f],
    "EI_MAG1": [0x45],
    "EI_MAG2": [0x4c],
    "EI_MAG3": [0x46],
    "EI_CLASS": [0x1],  # only 32
    "EI_DATA": [0x1],  # only little endian
    "EI_VERSION": [0x1],
    "EI_OSABI": [],
    "EI_ABIVERSION": [],
    "EI_PAD1": [],
    "EI_PAD2": [],
    "EI_PAD3": [],
    "EI_PAD4": [],
    "EI_PAD5": [],
    "EI_PAD6": [],
    "EI_PAD7": [],
}

match_header = {
    (16, 18): "E_TYPE",
    (18, 20): "E_MACHINE",
    (20, 24): "E_VERSION",
    (24, 28): "E_ENTRY",
    (28, 32): "E_PHOFF",
    (32, 36): "E_SHOFF",
    (36, 40): "E_FLAGS",
    (40, 42): "E_EHSIZE",
    (42, 44): "E_PHENTSIZE",
    (44, 46): "E_PHNUM",
    (46, 48): "E_SHENTSIZE",
    (48, 50): "E_SHNUM",
    (50, 52): "E_SHSTRNDX",
}

match_header_white_list = {
    "E_TYPE": [],
    "E_MACHINE": [],
    "E_VERSION": [],
    "E_ENTRY": [],
    "E_PHOFF": [],
    "E_SHOFF": [],
    "E_FLAGS": [],
    "E_EHSIZE": [0x34],  # only 32
    "E_PHENTSIZE": [0x20],  # only 32
    "E_PHNUM": [],
    "E_SHENTSIZE": [0x28],  # only 32
    "E_SHNUM": [],
    "E_SHSTRNDX": [],
}

# SECTIONS
match_section = {
    (0, 4): "SH_NAME",
    (4, 8): "SH_TYPE",
    (8, 12): "SH_FLAGS",
    (12, 16): "SH_ADDR",
    (16, 20): "SH_OFFSET",
    (20, 24): "SH_SIZE",
    (24, 28): "SH_LINK",
    (28, 32): "SH_INFO",
    (32, 36): "SH_ADDRALIGN",
    (36, 40): "SH_ENTSIZE",
}

match_symtab = {
    (0, 4): "NAME",
    (4, 8): "VALUE",
    (8, 12): "SIZE",
    (12, 13): "INFO",
    (13, 14): "OTHER",
    (14, 16): "SHNDX"
}

# SYMTAB
symtab_types = {
    0: "NOTYPE",
    1: "OBJECT",
    2: "FUNC",
    3: "SECTION",
    4: "FILE",
    5: "COMMON",
    6: "TLS",
    10: "LOOS",
    12: "HIOS",
    13: "LOPROC",
    15: "HIPROC"
}

symtab_binds = {
    0: "LOCAL",
    1: "GLOBAL",
    2: "WEAK",
    10: "LOOS",
    12: "HIOS",
    13: "LOPROC",
    15: "HIPROC"
}

symtab_vises = {
    0: "DEFAULT",
    1: "INTERNAL",
    2: "HIDDEN",
    3: "PROTECTED"
}

symtab_special = {
    0: "UNDEF",
    65280: "LOPROC",
    65311: "HIPROC",
    65312: "LOOS",
    65343: "HIOS",
    65521: "ABS",
    65522: "COMMON",
    65535: "HIRESERVE"
}

# TEXT
match_uncompress_command = {
    'R': {
        (0, 7): 'opcode',
        (7, 12): 'rd',
        (12, 15): 'funct3',
        (15, 20): 'rs1',
        (20, 25): 'rs2',
        (25, 32): 'funct7'
    },
    'I': {
        (0, 7): 'opcode',
        (7, 12): 'rd',
        (12, 15): 'funct3',
        (15, 20): 'rs1',
        (20, 32): 'imm11'
    },
    'S': {
        (0, 7): 'opcode',
        (7, 12): 'imm4',
        (12, 15): 'funct3',
        (15, 20): 'rs1',
        (20, 25): 'rs2',
        (25, 32): 'imm115'
    },
    'B': {
        (0, 7): 'opcode',
        (7, 12): 'imm4111',
        (12, 15): 'funct3',
        (15, 20): 'rs1',
        (20, 25): 'rs2',
        (25, 32): 'imm12105'
    },
    'U': {
        (0, 7): 'opcode',
        (7, 12): 'rd',
        (12, 32): 'imm3112'
    },
    'J': {
        (0, 7): 'opcode',
        (7, 12): 'rd',
        (12, 32): 'imm2010'
    },
    "CSR": {
        (0, 7): 'opcode',
        (7, 12): 'rd',
        (12, 15): 'funct3',
        (15, 20): 'rs1',
        (20, 32): 'csr'
    }
}

IMMS_UMCOMPRESS = {
    "I": lambda i: i,
    "S": lambda i, i2: i + i2,
    "B": lambda i, i2: i[0] + i2[-1] + i[1:] + i2[0:-1] + '0',
    "U": lambda i: i + '0' * 12,
    "J": lambda i: i[0] + i[-8:] + i[-9] + i[1:-9] + '0'  # imm[20|10:1|11|19:12]
}

ABI_REGISTERS = {
    (0, 1): 'zero',
    (1, 2): 'ra',
    (2, 3): 'sp',
    (3, 4): 'gp',
    (4, 5): 'tp',
    (5, 8): lambda i: 't' + str(i - 5),
    (8, 9): 's0',
    (9, 10): 's1',
    (10, 18): lambda i: "a" + str(i - 10),
    (18, 28): lambda i: "s" + str(i - 18 + 2),
    (28, 32): lambda i: "t" + str(i - 28 + 3)
}

base_uncompress = [
    {'type': 'CSR', 'opcode': '1110011', 'funct3': '001', 'name': 'csrrw'},
    {'type': 'CSR', 'opcode': '1110011', 'funct3': '010', 'name': 'csrrs'},
    {'type': 'CSR', 'opcode': '1110011', 'funct3': '011', 'name': 'csrrc'},
    {'type': 'CSR', 'opcode': '1110011', 'funct3': '101', 'name': 'csrrwi'},
    {'type': 'CSR', 'opcode': '1110011', 'funct3': '110', 'name': 'csrsi'},
    {'type': 'CSR', 'opcode': '1110011', 'funct3': '111', 'name': 'csrci'},
    {'type': 'U', 'opcode': '0110111', 'name': 'lui'},
    {'type': 'U', 'opcode': '0010111', 'name': 'auipc'},
    {'type': 'J', 'opcode': '1101111', 'name': 'jal'},
    {'type': 'I', 'funct3': '000', 'opcode': '1100111', 'name': 'jalr'},
    {'type': 'B', 'funct3': '000', 'opcode': '1100011', 'name': 'beq'},
    {'type': 'B', 'funct3': '001', 'opcode': '1100011', 'name': 'bne'},
    {'type': 'B', 'funct3': '100', 'opcode': '1100011', 'name': 'blt'},
    {'type': 'B', 'funct3': '101', 'opcode': '1100011', 'name': 'bge'},
    {'type': 'B', 'funct3': '110', 'opcode': '1100011', 'name': 'bltu'},
    {'type': 'B', 'funct3': '111', 'opcode': '1100011', 'name': 'bgeu'},
    {'type': 'I', 'funct3': '000', 'opcode': '0000011', 'name': 'lb'},
    {'type': 'I', 'funct3': '001', 'opcode': '0000011', 'name': 'lh'},
    {'type': 'I', 'funct3': '010', 'opcode': '0000011', 'name': 'lw'},
    {'type': 'I', 'funct3': '100', 'opcode': '0000011', 'name': 'lbu'},
    {'type': 'I', 'funct3': '101', 'opcode': '0000011', 'name': 'lhu'},
    {'type': 'S', 'funct3': '000', 'opcode': '0100011', 'name': 'sb'},
    {'type': 'S', 'funct3': '001', 'opcode': '0100011', 'name': 'sh'},
    {'type': 'S', 'funct3': '010', 'opcode': '0100011', 'name': 'sw'},
    {'type': 'I', 'funct3': '000', 'opcode': '0010011', 'name': 'addi'},
    {'type': 'I', 'funct3': '010', 'opcode': '0010011', 'name': 'slti'},
    {'type': 'I', 'funct3': '011', 'opcode': '0010011', 'name': 'sltiu'},
    {'type': 'I', 'funct3': '100', 'opcode': '0010011', 'name': 'xori'},
    {'type': 'I', 'funct3': '110', 'opcode': '0010011', 'name': 'ori'},
    {'type': 'I', 'funct3': '111', 'opcode': '0010011', 'name': 'andi'},
    {'type': 'R', 'funct3': '001', 'funct7': '0000000', 'opcode': '0010011', 'name': 'slli'},
    {'type': 'R', 'funct3': '101', 'funct7': '0000000', 'opcode': '0010011', 'name': 'srli'},
    {'type': 'R', 'funct3': '101', 'funct7': '0100000', 'opcode': '0010011', 'name': 'srai'},
    {'type': 'R', 'funct3': '000', 'funct7': '0000000', 'opcode': '0110011', 'name': 'add'},
    {'type': 'R', 'funct3': '000', 'funct7': '0100000', 'opcode': '0110011', 'name': 'sub'},
    {'type': 'R', 'funct3': '001', 'funct7': '0000000', 'opcode': '0110011', 'name': 'sll'},
    {'type': 'R', 'funct3': '010', 'funct7': '0000000', 'opcode': '0110011', 'name': 'slt'},
    {'type': 'R', 'funct3': '011', 'funct7': '0000000', 'opcode': '0110011', 'name': 'sltu'},
    {'type': 'R', 'funct3': '100', 'funct7': '0000000', 'opcode': '0110011', 'name': 'xor'},
    {'type': 'R', 'funct3': '101', 'funct7': '0000000', 'opcode': '0110011', 'name': 'srl'},
    {'type': 'R', 'funct3': '101', 'funct7': '0100000', 'opcode': '0110011', 'name': 'sra'},
    {'type': 'R', 'funct3': '110', 'funct7': '0000000', 'opcode': '0110011', 'name': 'or'},
    {'type': 'R', 'funct3': '111', 'funct7': '0000000', 'opcode': '0110011', 'name': 'and'},
    {'type': 'I', 'funct3': '000', 'opcode': '1110011', 'name': 'ecall'},
    {'type': 'I', 'funct3': '000', 'opcode': '1110011', 'name': 'ebreak'},
    {'type': 'R', 'funct3': '000', 'funct7': '0000001', 'opcode': '0110011', 'name': 'mul'},
    {'type': 'R', 'funct3': '001', 'funct7': '0000001', 'opcode': '0110011', 'name': 'mulh'},
    {'type': 'R', 'funct3': '010', 'funct7': '0000001', 'opcode': '0110011', 'name': 'mulhsu'},
    {'type': 'R', 'funct3': '011', 'funct7': '0000001', 'opcode': '0110011', 'name': 'mulhu'},
    {'type': 'R', 'funct3': '100', 'funct7': '0000001', 'opcode': '0110011', 'name': 'div'},
    {'type': 'R', 'funct3': '101', 'funct7': '0000001', 'opcode': '0110011', 'name': 'divu'},
    {'type': 'R', 'funct3': '110', 'funct7': '0000001', 'opcode': '0110011', 'name': 'rem'},
    {'type': 'R', 'funct3': '111', 'funct7': '0000001', 'opcode': '0110011', 'name': 'remu'}
]

opcodes_type = {'U': {'0110111', '0010111'},
                'J': {'1101111'},
                'I': {'0000011', '1100111', '0010011'},
                'B': {'1100011'},
                'S': {'0100011'},
                'R': {'0110011', '0010011'},
                "CSR": {'1110011'}
                }

I_type_except = ['lb', 'lh', 'lw', 'lbu', 'lhu']
I_control = ['ecall', 'ebreak']
R_type_except = ['srai', 'srli', 'slli']

# SLLI SRLI SRAI
RI_conflict = '0010011'
funct3_R = ['001', '101']
funct3_I = ['000', '010', '011', '100', '110', '111']


# ECALL EBREAK , CSR
e_opcode = '1110011'

compress = {('00', '000'): 'ADDI4SPN', ('00', '001'): 'FLD', ('00', '010'): 'LW', ('00', '011'): 'FLW',
            ('00', '100'): 'Reserved', ('00', '101'): 'FSD', ('00', '110'): 'SW', ('00', '111'): 'FSW',
            ('01', '000'): 'ADDI', ('01', '001'): 'JAL', ('01', '010'): 'LI', ('01', '011'): 'LUI/ADDI16SP',
            ('01', '100'): 'MISC-ALU', ('01', '101'): 'J', ('01', '110'): 'BEQZ', ('01', '111'): 'BNEZ',
            ('10', '000'): 'SLLI', ('10', '001'): 'FLDSP', ('10', '010'): 'LWSP', ('10', '011'): 'FLWSP',
            ('10', '100'): 'J[AL]R/MV/ADD', ('10', '101'): 'FSDSP', ('10', '110'): 'SWSP', ('10', '111'): 'FSWSP'}

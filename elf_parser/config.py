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
nop = '10011'.rjust(32, '0')
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
    # "CSR": {
    #     (0, 7): 'opcode',
    #     (7, 12): 'rd',
    #     (12, 15): 'funct3',
    #     (15, 20): 'rs1',
    #     (20, 32): 'csr'
    # }
}

IMMS_UMCOMPRESS = {
    "I": lambda i: i,
    "S": lambda i, i2: i + i2,
    "B": lambda i, i2: i[0] + i2[-1] + i[1:] + i2[0:-1] + '0',
    "U": lambda i: i,
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

# i deadinside
csr_opcode = '1110011'
csr_alot_registers = {
    (0xC03, 0xC1F): lambda i: f'hpmcounter{int(i, 16) - 0xC00}',
    (0xC84, 0xC9F): lambda i: f'hpmcounter{int(i, 16) - 0xC81}h',
    (0xB03, 0xB1F): lambda i: f'mhpmcounter{int(i, 16) - 0xB00}',
    (0x323, 0x33F): lambda i: f'mhpmevent{int(i, 16) - 0x320}'

}
csr_registers = {'0x000': 'ustatus', '0x004': 'uie', '0x005': 'utvec', '0x040': 'uscratch', '0x041': 'uepc', '0x042': 'ucause', '0x043': 'ubadaddr', '0x044': 'uip', '0x001': 'fflags', '0x002': 'frm', '0x003': 'fcsr', '0xc00': 'cycle', '0xc01': 'time', '0xc02': 'instret', '0xc80': 'cycleh', '0xc81': 'timeh', '0xc82': 'instreth', '0x100': 'sstatus', '0x102': 'sedeleg', '0x103': 'sideleg', '0x104': 'sie', '0x105': 'stvec', '0x140': 'sscratch', '0x141': 'sepc', '0x142': 'scause', '0x143': 'sbadaddr', '0x144': 'sip', '0x180': 'sptbr', '0x200': 'hstatus', '0x202': 'hedeleg', '0x203': 'hideleg', '0x204': 'hie', '0x205': 'htvec', '0x240': 'hscratch', '0x241': 'hepc', '0x242': 'hcause', '0x243': 'hbadaddr', '0x244': 'hip', '0x28x': 'tbd', '0xf11': 'mvendorid', '0xf12': 'marchid', '0xf13': 'mimpid', '0xf14': 'mhartid', '0x300': 'mstatus', '0x301': 'misa', '0x302': 'medeleg', '0x303': 'mideleg', '0x304': 'mie', '0x305': 'mtvec', '0x340': 'mscratch', '0x341': 'mepc', '0x342': 'mcause', '0x343': 'mbadaddr', '0x344': 'mip', '0x380': 'mbase', '0x381': 'mbound', '0x382': 'mibase', '0x383': 'mibound', '0x384': 'mdbase', '0x385': 'mdbound', '0xb00': 'mcycle', '0xb02': 'minstret', '0xb80': 'mcycleh', '0xb82': 'minstreth', '0x320': 'mucounteren', '0x321': 'mscounteren', '0x322': 'mhcounteren', '0x7a0': 'tselect', '0x7a1': 'tdata1', '0x7a2': 'tdata2', '0x7a3': 'tdata3', '0x7b0': 'dcsr', '0x7b1': 'dpc', '0x7b2': 'dscratch'}


base_uncompress = [
    {'type': 'I', 'opcode': '1110011', 'funct3': '001', 'name': 'csrrw'},
    {'type': 'I', 'opcode': '1110011', 'funct3': '010', 'name': 'csrrs'},
    {'type': 'I', 'opcode': '1110011', 'funct3': '011', 'name': 'csrrc'},
    {'type': 'I', 'opcode': '1110011', 'funct3': '101', 'name': 'csrrwi'},
    {'type': 'I', 'opcode': '1110011', 'funct3': '110', 'name': 'csrsi'},
    {'type': 'I', 'opcode': '1110011', 'funct3': '111', 'name': 'csrci'},
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
    {'type': 'I', 'funct3': '000', 'opcode': '0001111', 'name': 'fence'},
    {'type': 'I', 'funct3': '000', 'opcode': '1110011', 'name': 'ebreak'},
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
                'I': {'0000011', '1100111', '0010011', '1110011', '0001111'},
                'B': {'1100011'},
                'S': {'0100011'},
                'R': {'0110011', '0010011'},
                "CSR": {''}
                }

I_type_except = ['lb', 'lh', 'lw', 'lbu', 'lhu', 'jalr']
I_control = ['ecall', 'ebreak', 'fence']
R_type_except = ['srai', 'srli', 'slli']

# SLLI SRLI SRAI
RI_conflict = '0010011'
funct3_R = ['001', '101']
funct3_I = ['000', '010', '011', '100', '110', '111']


# ECALL EBREAK , CSR
e_opcode = '1110011'

compress_names = {
    ('00', '000'): 'addi4spn',
    ('00', '001'): 'fld',
    ('00', '010'): 'lw',
    ('00', '011'): 'flw',
    ('00', '100'): 'reserved',
    ('00', '101'): 'fsd',
    ('00', '110'): 'sw',
    ('00', '111'): 'fsw',
    ('01', '000'): 'addi',
    ('01', '001'): 'jal',
    ('01', '010'): 'li',
    ('01', '011'): 'lui/addi16sp',
    ('01', '100'): 'misc-alu',
    ('01', '101'): 'j',
    ('01', '110'): 'beqz',
    ('01', '111'): 'bnez',
    ('10', '000'): 'slli',
    ('10', '001'): 'fldsp',
    ('10', '010'): 'lwsp',
    ('10', '011'): 'flwsp',
    ('10', '100'): 'j[al]r/mv/add',
    ('10', '101'): 'fsdsp',
    ('10', '110'): 'swsp',
    ('10', '111'): 'fswsp'
}
# 0 1 2 3 4 5 6 7
# 5 4 9 8 7 6 2 3
match_compress = {
    'r42': lambda i: i[-5: -2],
    'r97': lambda i: i[-10: -7],
    'r512': lambda i: i[-13: -5],
    'immasp': lambda i: i
}


formats = {
    ('sw', 'sh', 'sb'): "{name} {}"
}

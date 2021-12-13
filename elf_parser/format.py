math_e_ident = {
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

# symtab
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

# text
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
        (20, 32): 'imm[11:0]'
    },
    'S': {
        (0, 7): 'opcode',
        (7, 12): 'imm[4:0]',
        (12, 15): 'funct3',
        (15, 20): 'rs1',
        (20, 25): 'rs2',
        (25, 32): 'imm[11:5]'
    },
    'B': {
        (0, 7): 'opcode',
        (7, 12): 'imm[12|10:5]',
        (12, 15): 'funct3',
        (15, 20): 'rs1',
        (20, 25): 'rs2',
        (25, 32): 'imm[4:1|11]'
    },
    'U': {
        (0, 7): 'opcode',
        (7, 12): 'rd',
        (12, 32): 'imm[31:12]'
    },
    'J': {
        (0, 7): 'opcode',
        (7, 12): 'rd',
        (12, 32): 'imm[20|10:1|11|19:12]'
    },
}

base_uncompress = [
    {'type': 'U', 'opcode': '0110111', 'name': 'LUI'},
    {'type': 'U', 'opcode': '0010111', 'name': 'AUIPC'},
    {'type': 'J', 'opcode': '1101111', 'name': 'JAL'},
    {'type': 'I', 'funct3': '000', 'opcode': '1100111', 'name': 'JALR'},
    {'type': 'B', 'funct3': '000', 'opcode': '1100011', 'name': 'BEQ'},
    {'type': 'B', 'funct3': '001', 'opcode': '1100011', 'name': 'BNE'},
    {'type': 'B', 'funct3': '100', 'opcode': '1100011', 'name': 'BLT'},
    {'type': 'B', 'funct3': '101', 'opcode': '1100011', 'name': 'BGE'},
    {'type': 'B', 'funct3': '110', 'opcode': '1100011', 'name': 'BLTU'},
    {'type': 'B', 'funct3': '111', 'opcode': '1100011', 'name': 'BGEU'},
    {'type': 'I', 'funct3': '000', 'opcode': '0000011', 'name': 'LB'},
    {'type': 'I', 'funct3': '001', 'opcode': '0000011', 'name': 'LH'},
    {'type': 'I', 'funct3': '010', 'opcode': '0000011', 'name': 'LW'},
    {'type': 'I', 'funct3': '100', 'opcode': '0000011', 'name': 'LBU'},
    {'type': 'I', 'funct3': '101', 'opcode': '0000011', 'name': 'LHU'},
    {'type': 'S', 'funct3': '000', 'opcode': '0100011', 'name': 'SB'},
    {'type': 'S', 'funct3': '001', 'opcode': '0100011', 'name': 'SH'},
    {'type': 'S', 'funct3': '010', 'opcode': '0100011', 'name': 'SW'},
    {'type': 'I', 'funct3': '000', 'opcode': '0010011', 'name': 'ADDI'},
    {'type': 'I', 'funct3': '010', 'opcode': '0010011', 'name': 'SLTI'},
    {'type': 'I', 'funct3': '011', 'opcode': '0010011', 'name': 'SLTIU'},
    {'type': 'I', 'funct3': '100', 'opcode': '0010011', 'name': 'XORI'},
    {'type': 'I', 'funct3': '110', 'opcode': '0010011', 'name': 'ORI'},
    {'type': 'I', 'funct3': '111', 'opcode': '0010011', 'name': 'ANDI'},
    {'type': 'R', 'funct3': '001', 'funct7': '0000000', 'opcode': '0010011', 'name': 'SLLI'},
    {'type': 'R', 'funct3': '101', 'funct7': '0000000', 'opcode': '0010011', 'name': 'SRLI'},
    {'type': 'R', 'funct3': '101', 'funct7': '0100000', 'opcode': '0010011', 'name': 'SRAI'},
    {'type': 'R', 'funct3': '000', 'funct7': '0000000', 'opcode': '0110011', 'name': 'ADD'},
    {'type': 'R', 'funct3': '000', 'funct7': '0100000', 'opcode': '0110011', 'name': 'SUB'},
    {'type': 'R', 'funct3': '001', 'funct7': '0000000', 'opcode': '0110011', 'name': 'SLL'},
    {'type': 'R', 'funct3': '010', 'funct7': '0000000', 'opcode': '0110011', 'name': 'SLT'},
    {'type': 'R', 'funct3': '011', 'funct7': '0000000', 'opcode': '0110011', 'name': 'SLTU'},
    {'type': 'R', 'funct3': '100', 'funct7': '0000000', 'opcode': '0110011', 'name': 'XOR'},
    {'type': 'R', 'funct3': '101', 'funct7': '0000000', 'opcode': '0110011', 'name': 'SRL'},
    {'type': 'R', 'funct3': '101', 'funct7': '0100000', 'opcode': '0110011', 'name': 'SRA'},
    {'type': 'R', 'funct3': '110', 'funct7': '0000000', 'opcode': '0110011', 'name': 'OR'},
    {'type': 'R', 'funct3': '111', 'funct7': '0000000', 'opcode': '0110011', 'name': 'AND'},
    {'type': 'I', 'funct3': '000', 'opcode': '1110011', 'name': 'ECALL'},
    {'type': 'I', 'funct3': '000', 'opcode': '1110011', 'name': 'EBREAK'},
    {'type': 'R', 'funct3': '000', 'funct7': '0000001', 'opcode': '0110011', 'name': 'MUL'},
    {'type': 'R', 'funct3': '001', 'funct7': '0000001', 'opcode': '0110011', 'name': 'MULH'},
    {'type': 'R', 'funct3': '010', 'funct7': '0000001', 'opcode': '0110011', 'name': 'MULHSU'},
    {'type': 'R', 'funct3': '011', 'funct7': '0000001', 'opcode': '0110011', 'name': 'MULHU'},
    {'type': 'R', 'funct3': '100', 'funct7': '0000001', 'opcode': '0110011', 'name': 'DIV'},
    {'type': 'R', 'funct3': '101', 'funct7': '0000001', 'opcode': '0110011', 'name': 'DIVU'},
    {'type': 'R', 'funct3': '110', 'funct7': '0000001', 'opcode': '0110011', 'name': 'REM'},
    {'type': 'R', 'funct3': '111', 'funct7': '0000001', 'opcode': '0110011', 'name': 'REMU'},
]

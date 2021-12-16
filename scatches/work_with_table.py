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

opcodes_types = {}

for i in base_uncompress:
    if i['type'] not in opcodes_types:
        opcodes_types.update({i['type']: []})
    opcodes_types[i['type']].append(i['opcode'])

for i in opcodes_types:
    opcodes_types[i] = set(opcodes_types[i])
print(opcodes_types)


# jal


# addi4spn
# lw
# reserved
# sw
# addi
# li
# lui/addi16sp

# misc-alu
# j


# beqz
# bnez

# slli

# lwsp
# swsp

# j[al]r/mv/add
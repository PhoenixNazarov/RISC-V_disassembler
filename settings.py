# Settings
name_section_of_riscv = '.text.init'  # '.text.init'

# Out formats
symtab_name = "{} {:15} {:>5} {:8} {:8} {:8} {:>6} {}\n".format(
    'Symbol',
    'Value',
    'Size',
    'Type',
    'Bind',
    'Vis',
    'Index',
    'Name'
)

symtab_data = "[{numb:>4}] {value:15} {size:>5} {type:8} {bind:8} {vis:8} {index:>6} {name}\n"
command_data = "{:08x} {:>20} {} {}\n"

# Command
rvc_prefix = 'c.'
unknown = 'unknown_command'
unknown_rvc = 'unknown_compress'


# dec, hex
U_NOTION = 'dec'
BJ_NOTION = 'dec'
SSS_NOTION = 'dec'  # for srai', 'srli', 'slli

BJ_VAL = 'offset'      # addr, offset
LOC_VAL = "addr"   # addr, count


# Make pseudoinstruction
nop = True
rvc_illegal_instruction = 'unimp'  # when rvc is 0x0

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
command_data = "{:08x} {:>20}: {} {}\n"

# Command
new_lock_name_type = 'addr'  # count, addr
branch_jump_out_type = 'addr_hex'  # addr_hex, offset_dec, addr_dec
u_imm_dec_type = False

# Make pseudoinstruction
nop = False
rvc_illegal_instruction = 'unimp'  # when rvc is 0x0

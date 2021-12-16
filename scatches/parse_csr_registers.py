a = """
0x000 URW ustatus User status register.
0x004 URW uie User interrupt-enable register.
0x005 URW utvec User trap handler base address.
0x040 URW uscratch Scratch register for user trap handlers.
0x041 URW uepc User exception program counter.
0x042 URW ucause User trap cause.
0x043 URW ubadaddr User bad address.
0x044 URW uip User interrupt pending.
0x001 URW fflags Floating-Point Accrued Exceptions.
0x002 URW frm Floating-Point Dynamic Rounding Mode.
0x003 URW fcsr Floating-Point Control and Status Register (frm + fflags).
0xC00 URO cycle Cycle counter for RDCYCLE instruction.
0xC01 URO time Timer for RDTIME instruction.
0xC02 URO instret Instructions-retired counter for RDINSTRET instruction.
0xC80 URO cycleh Upper 32 bits of cycle, RV32I only.
0xC81 URO timeh Upper 32 bits of time, RV32I only.
0xC82 URO instreth Upper 32 bits of instret, RV32I only.
0x100 SRW sstatus Supervisor status register.
0x102 SRW sedeleg Supervisor exception delegation register.
0x103 SRW sideleg Supervisor interrupt delegation register.
0x104 SRW sie Supervisor interrupt-enable register.
0x105 SRW stvec Supervisor trap handler base address.
0x140 SRW sscratch Scratch register for supervisor trap handlers.
0x141 SRW sepc Supervisor exception program counter.
0x142 SRW scause Supervisor trap cause.
0x143 SRW sbadaddr Supervisor bad address.
0x144 SRW sip Supervisor interrupt pending.
0x180 SRW sptbr Page-table base register.
0x200 HRW hstatus Hypervisor status register.
0x202 HRW hedeleg Hypervisor exception delegation register.
0x203 HRW hideleg Hypervisor interrupt delegation register.
0x204 HRW hie Hypervisor interrupt-enable register.
0x205 HRW htvec Hypervisor trap handler base address.
0x240 HRW hscratch Scratch register for hypervisor trap handlers.
0x241 HRW hepc Hypervisor exception program counter.
0x242 HRW hcause Hypervisor trap cause.
0x243 HRW hbadaddr Hypervisor bad address.
0x244 HRW hip Hypervisor interrupt pending.
0x28X TBD TBD TBD.
0xF11 MRO mvendorid Vendor ID.
0xF12 MRO marchid Architecture ID.
0xF13 MRO mimpid Implementation ID.
0xF14 MRO mhartid Hardware thread ID.
0x300 MRW mstatus Machine status register.
0x301 MRW misa ISA and extensions
0x302 MRW medeleg Machine exception delegation register.
0x303 MRW mideleg Machine interrupt delegation register.
0x304 MRW mie Machine interrupt-enable register.
0x305 MRW mtvec Machine trap-handler base address.
0x340 MRW mscratch Scratch register for machine trap handlers.
0x341 MRW mepc Machine exception program counter.
0x342 MRW mcause Machine trap cause.
0x343 MRW mbadaddr Machine bad address.
0x344 MRW mip Machine interrupt pending.
0x380 MRW mbase Base register.
0x381 MRW mbound Bound register.
0x382 MRW mibase Instruction base register.
0x383 MRW mibound Instruction bound register.
0x384 MRW mdbase Data base register.
0x385 MRW mdbound Data bound register.
0xB00 MRW mcycle Machine cycle counter.
0xB02 MRW minstret Machine instructions-retired counter.
0xB80 MRW mcycleh Upper 32 bits of mcycle, RV32I only.
0xB82 MRW minstreth Upper 32 bits of minstret, RV32I only.
0x320 MRW mucounteren User-mode counter enable.
0x321 MRW mscounteren Supervisor-mode counter enable.
0x322 MRW mhcounteren Hypervisor-mode counter enable.
0x7A0 MRW tselect Debug/Trace trigger register select.
0x7A1 MRW tdata1 First Debug/Trace trigger data register.
0x7A2 MRW tdata2 Second Debug/Trace trigger data register.
0x7A3 MRW tdata3 Third Debug/Trace trigger data register.
0x7B0 DRW dcsr Debug control and status register.
0x7B1 DRW dpc Debug PC.
0x7B2 DRW dscratch Debug scratch register.
"""

g = {}
for i in a.split('\n')[1:-1]:
    b = i.split(' ')
    key, name = b[0], b[2]
    g.update({key: name})
print(g)

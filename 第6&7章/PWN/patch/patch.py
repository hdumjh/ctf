def patch_call(target,begin,arch = "amd64"):
	order = ((target - (begin + 5 )) & 0xffffffff)
	order_s = hex(order)[2:].upper().rjust(8,"0")
	res = ""
	for i in range(8,0,-2):
		res += " " + order_s[i-2:i] 
	print "E8" + res
	print hex(order)

patch_call(0x00000000004008D0,0x0000000000400755)
patch_call(0x0000000000400570,0x00000000004008D8)
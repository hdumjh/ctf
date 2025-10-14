all:
	gcc -Wl,-z,lazy -no-pie -fno-stack-protector -m32 -z execstack  ret2shellcode.c -o ret2shellcode
clean:
	rm -rf ret2text ret2shellcode.o


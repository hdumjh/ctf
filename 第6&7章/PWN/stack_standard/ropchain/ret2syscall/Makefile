all:
	gcc -Wl,-z,lazy -no-pie -fno-stack-protector -m32 -static ret2syscall.c -o ret2syscall
clean:
	rm -rf ret2syscall ret2syscall.o


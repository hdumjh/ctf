all:
	gcc -Wl,-z,lazy -no-pie -m32 -fstack-protector-all leak_canary.c -o leak_canary
clean:
	rm -rf leak_canary leak_canary.o


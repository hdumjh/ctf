all:
	gcc -Wl,-z,lazy -pie -z noexecstack -fstack-protector-all tcache_double_free.c -o tcache_double_free
clean:
	rm -rf tcache_double_free tcache_double_free.o


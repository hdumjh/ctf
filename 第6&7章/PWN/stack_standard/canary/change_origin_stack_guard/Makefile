all:
	gcc -Wl,-z,lazy -no-pie -fstack-protector-all -pthread change_origin_stack_guard.c -o change_origin_stack_guard
clean:
	rm -rf change_origin_stack_guard change_origin_stack_guard.o


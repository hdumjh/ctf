#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char adjust[0x300] = {0};
char magic[12] = {0};

void target(){
	system("/bin/sh");
}

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void input_name(char *buf){
	puts("leave your name");
	read(0,magic,12);
	memcpy(buf,magic,12);
}

void vulnfunc(){
	char *buf;
	puts("stack pivoting - change ebp");
	__asm__("LEA -8(%ebp), %eax;"
		"PUSH %eax;"
		"CALL input_name;"
	);
}

void call_vunlfunc(){
	vulnfunc();
}

int main(){
	init();
	call_vunlfunc();
}

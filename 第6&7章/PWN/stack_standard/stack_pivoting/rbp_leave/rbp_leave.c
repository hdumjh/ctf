#include <stdio.h>
#include <stdlib.h>

char name[0x400] = {0};

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void read_input(char *addr, int length){
	read(0,addr,length);
}

void vulnfunc() {
	char buf[0x100];
	puts("change rbp & leave ret");
	puts("leave your name");
	read_input(name,0x400);
	puts("try to break it");
	read_input(buf,0x110);
}

int main(){	
	init();
	vulnfunc();
}

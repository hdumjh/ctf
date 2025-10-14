#include <stdio.h>
#include <stdlib.h>

void target(){
	system("try to make a binsh");
}

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void vulnfunc() {
	char buf[0x100];
	puts("ret2libc2");
	gets(buf);
}

int main(){	
	init();
	vulnfunc();
}

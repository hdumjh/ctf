#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void vulnfunc() {
	char buf[0x100];
	write(1,"ret2_libc_csu_init\n",strlen("ret2_libc_csu_init\n"));
	read(0,buf,0x200);
}

int main(){	
	init();
	vulnfunc();
}

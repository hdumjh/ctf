#include <stdio.h>
#include <stdlib.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void vulnfunc() {
	char buf[0x100];
	while (1){
		read(0,buf,0x100);	
		printf(buf);
	}
}

int main(){	
	init();
	vulnfunc();
}

#include <stdio.h>
#include <stdlib.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void vulnfunc() {
	char buf[0x100];
	scanf("%100s",buf);
	printf(buf);
}

int main(){	
	init();
	vulnfunc();
}

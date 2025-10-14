#include <stdio.h>
#include <stdlib.h>

int b = 0xdead,c = 0xbeef;

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void vulnfunc() {
	char buf[0x100];
	int a = 0xdeadbeef;
	printf("%p\n",&a);
	scanf("%100s",buf);
	printf(buf);
	if (a == 0x10){
		puts("overwrite a for a regular value");
	}
	else if (b == 2){
		puts("overwrite b for a small value");
	}
	else if (c == 0x12345678){
		puts("overwrite c for a big value");	
	}
}

int main(){	
	init();
	vulnfunc();
}

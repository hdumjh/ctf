#include <stdio.h>
#include <stdlib.h>

char flag[30] = {0};

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void vulnfunc() {
	char buf[0x100];
	FILE *fp;
	
	fp = fopen("./flag","rw");
	if (fp == NULL){
		puts("file open failed");
		return;
	}
	fread(flag,30,1,fp);
	puts("stack_smashes");
	read(0,buf,0x300);
}

int main(){	
	init();
	vulnfunc();
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void magic(){
	system("/bin/sh");
}

void vulnfunc(){
	int size,offset;
	char *p;
	char data[0x80] = {0};
	puts("babyheap test for add logic");
	puts("give me your name size");
	scanf("%d",&size);
	getchar();
	if(size > 0x100){
		puts("size too big");
		exit(0);	
	}
	p = malloc(size);
	puts("give me a offset");
	scanf("%d",&offset);
	getchar();
	read(0,p + offset,0x10);
	puts("good bye");
}

int main(int argc, char const *argv[],char const *env[])
{
	init();	
	vulnfunc();
	return 0;
}

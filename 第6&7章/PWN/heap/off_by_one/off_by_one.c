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
	char buf[0x20] = {0};
	init();
	// malloc three chunk
	p = malloc(0x18);
	q = malloc(0x18);
	r = malloc(0x18);
	sleep(0);
	// off by one
	strcpy(buf,"aaaaaaaabbbbbbbbcccccccc");
	buf[0x18] = 0x41;
	memcpy(p,buf,0x19);
	sleep(0);
	// free and then malloc
	free(q);
	q = malloc(0x38);
	// q has same space as r
	printf("%p\n",q);
	printf("%p\n",r);
	sleep(0);
}


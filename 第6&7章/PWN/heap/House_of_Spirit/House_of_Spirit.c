#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

long long data[0x20] = {0};

int main(){	
	int size = 0x70;
	void *p;
	init();
	// init arena
	malloc(0);
	// fake chunk header
	printf("%p\n",data);
	data[0] = 0x0;
	data[1] = size | 1; // prev_inuse_bit
	// fake next chunk header
	data[size / 8] = 0x0;
	data[(size / 8) + 1] = 0x11;
	sleep(0);
	// free user data place, fd.
	free(&data[2]);
	sleep(0);
	// user's size == chunk_size - 0x10
	p = malloc(size - 0x10);
	printf("%p\n",p);
	sleep(0);
}


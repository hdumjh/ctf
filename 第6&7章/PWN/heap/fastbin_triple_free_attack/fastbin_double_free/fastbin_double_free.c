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
	long *p;
	// init a chunk
	init();
	p = malloc(0x68);
	free(p);
	free(p);
}


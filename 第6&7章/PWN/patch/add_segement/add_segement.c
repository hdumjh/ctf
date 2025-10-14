#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void vulnfunc(){
	char buf[0x80];
	puts("babyfmt test for add segement");
	puts("enjoy the game");
	read(0,buf,0x80);
	printf(buf);
	puts("next time");
	read(0,buf,0x80);
	printf(buf);
}

int main(int argc, char const *argv[],char const *env[])
{
	init();	
	vulnfunc();
	return 0;
}

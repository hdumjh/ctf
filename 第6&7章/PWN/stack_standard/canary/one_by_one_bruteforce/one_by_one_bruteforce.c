#include <stdio.h>
#include <stdlib.h>

char cmd[] = "/bin/sh";

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void target(){
	system("/bin/sh");
}

void vulnfunc() {
	char buf[0x100];
	int childpid;

	while(1){
		if (fork() == 0){
			//child process
			puts("one_by_one_bruteforce");
			read(0,buf,0x200);
			return;
		}else{
			//parent process
			wait();
			puts("are you ready?");
			read(0,buf,2);
			if (buf[0] == 'y'){
				break;
			}
		}
	}
	puts("go");
	read(0,buf,0x200);
}

int main(){	
	init();
	vulnfunc();
}

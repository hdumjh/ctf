#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

char cmd[] = "/bin/sh";

void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
}

void target(){
	system(cmd);
}

void thr_fn(){
	char buf[0x100];
	puts("change the origin stack guard");
	read(0,buf,0x10000);
}

void vulnfunc() {
	int err;
	pthread_t ntid;
	
	err = pthread_create(&ntid, NULL, thr_fn, NULL);
	if (err != 0){
		puts("create thread error");
	}
	err = pthread_join(ntid,NULL);
	if (err != 0){
		puts("exit fail");	
	}
	puts("exit normally");
}

int main(){	
	init();
	vulnfunc();
}

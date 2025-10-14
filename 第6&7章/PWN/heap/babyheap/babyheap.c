#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "unistd.h"
#define MAX_SIZE 0x10

char *list[MAX_SIZE] = {0};
void init() {
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 1, 0);
	setvbuf(stderr, 0, 1, 0);
	alarm(0x30);
}

void menu(){
	puts("1.add");
	puts("2.edit");
	puts("3.show");
	puts("4.delete");
	puts("5.exit");
	puts(">> ");
}

int getint(){
	char buf[0xA];
	read(0,buf,0xA);
	return atoi(buf);
}

void read_input(char *addr,int length){
	int i;
	for(i = 0;i < length; i++){
		read(0,addr + i,1);
		if (*(addr + i) == '\n'){
			*(addr + i) = '\x00';
			break;
		}
	}
}

int add(){
	int index,i,size;
	for(i = 0;i < MAX_SIZE;i++){
		if (list[i] == NULL){
			break;
		}
	}
	if (i == MAX_SIZE){
		puts("list full\n");
		return 0;
	}
	puts("input your name size");
	size = getint();
	if (size < 0 || size > 0x500){
		puts("invalid size");
		return 0;
	}
	list[i] = malloc(size);
	puts("input your name");
	read_input(list[i],size);
	return 0;
}

int edit(){
	int index,size;
	puts("input index");
	index = getint();
	if (index < 0 || index > MAX_SIZE){
		puts("invalid index");
		return 0;
	}
	puts("input your name size");
	size = getint();
	if (list[index]){
		puts("input your name");
		read_input(list[index],size);
	}
	return 0;
}

int show(){
	int index;
	puts("input index");
	index = getint();
	if (index < 0 || index > MAX_SIZE){
		puts("invalid index");
		return 0;
	}
	if (list[index]){
		puts(list[index]);
	}
	return 0;
}

int delete(){
	int index;
	puts("input index");
	index = getint();
	if (index < 0 || index > MAX_SIZE){
		puts("invalid index");
		return 0;
	}
	if (list[index]){
		free(list[index]);
		list[index] = 0;
	}
	return 0;
}

int main(int argc, char const *argv[],char const *env[])
{
	int index;
	init();
	while (1){
		menu();
		index = getint();
		switch(index){
			case 1:
				add();
				break;
			case 2:
				edit();
				break;
			case 3:
				show();
				break;
			case 4:
				delete();
				break;
			case 5:
				return 0;
			default:
				puts("invalid choice");
		}
	}
	return 0;
}

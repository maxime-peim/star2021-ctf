#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

//gcc -o shlc3 shlc3.c -no-pie -fno-stack-protector -m32 -z execstack

void vuln(){
        char buffer[60];
        puts("What material should we use to create our houses?");
        fgets(buffer, 60, stdin);
        ((void (*)())buffer)();
}

void main(){
	vuln();
}


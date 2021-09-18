#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>

//gcc -o canary2 canary2.c -no-pie -fno-stack-protector -m32
char canary[4];

void get_canary(){
        FILE *fp = fopen("/home/pwn3r/canary.txt", "r");
        if(fp){
                fread(canary,1,sizeof(canary), fp);
        }
        else{
                puts("Error, contact the admins please.");
        }
}
void vuln(){
        int win = 0;
        char gorfou_y[4];
        //Now, people don't know its value
        memcpy(gorfou_y, canary, 4);
        char buffer[40];
        puts("Now, the gorfou is trying to cross the road again!");
        read(0,buffer, 60);
        if (strncmp(gorfou_y,canary,4)){
                puts("A car smashed the gorfou :(");
                exit(0);
        }
        if (win){
		setregid(getegid(), getegid());
                system("/bin/sh");
        }
}

void main(){
        get_canary();
        vuln();
}


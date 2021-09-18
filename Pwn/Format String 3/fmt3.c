#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

//gcc -o fmt3 fmt3.c -no-pie -m32 -z execstack -fstack-protector-all

void vuln(){
        int canard = 0x9badbad9;
        char buffer[80];
        printf("We have detected other canards at %p!\n", &canard);
        printf("Shoot them: \n");
        fgets(buffer, sizeof(buffer), stdin);
        printf("Understood, let's shoot at: ");
        printf(buffer);
        puts("Missile sent!");
}

void main(){
        setregid(getegid(), getegid());
	vuln();
}


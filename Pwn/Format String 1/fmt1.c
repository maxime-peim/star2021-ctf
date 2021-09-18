#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

//gcc -o fmt1 fmt1.c -no-pie -m32

char flag[32];

void vuln(){
        char buffer[50];
        printf("A wild gorfou appeared: ");
        fgets(buffer, sizeof(buffer), stdin);
        printf("The gorfou repeated: ");
        printf(buffer); //don't need anything else, it works fine
}
void main(){
        FILE *fp = fopen("/home/pwn3r/flag", "r");
        if(fp){
                fgets(flag,sizeof(flag),fp);
        }
        else{
                puts("Error, contact the admins please.");
        }
        vuln();
}


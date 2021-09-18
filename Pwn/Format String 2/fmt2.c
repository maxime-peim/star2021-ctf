#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

//gcc -o fmt2 fmt2.c -no-pie -m32 -fstack-protector-all

void vuln(){
        int canard = 0x3badbad3;
        char buffer[50];
        printf("We have detected canards at %p", &canard);
        printf(". They are the ennemies of the gorfous. Shoot them: \n");
        fgets(buffer, sizeof(buffer), stdin);
        printf("Understood, let's shoot at: ");
        printf(buffer);
        if (canard == 0xabababab){
                puts("You shot him! Yippeee!");
		setregid(getegid(), getegid());
                system("/bin/sh");
        }
        else if (canard == 0x3badbad3){
                puts("You missed the canards. Fly, you fools!");
        }
        else {
                puts("Close! They lost some feathers!");
        }

}
void main(){
        vuln();
}


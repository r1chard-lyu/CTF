#include <stdio.h>
#include <unistd.h>


char fn[0x20];
char ROP[0x100];


// fd = open("flag", 0);
// read(fd, buf, 0x30);
// write(1, buf, 0x30); // 1 --> stdout

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);


    printf("Give me filename: ");
    read(0, fn, 0x20);

    printf("Give me ROP: ");
    read(0, ROP, 0x100);

    char overflow[0x10];
    printf("Give me overflow: ");
    read(0, overflow, 0x30);

    return 0;
}

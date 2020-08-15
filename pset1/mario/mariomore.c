// This program prints a pyramid of bricks

//Calls library
#include <cs50.h>
#include <stdio.h>

// Create function 'repeat'
void repeat(char c, int times)
{
    while (--times >= 0)
    {
        printf("%c", c);
    }
}

//Runs main program
int main(void)
{
    //Prompts the user to insert pyramid height
    int h, w;
    do
    {
        h = get_int("Pyramid heigh: ");
        w = h;
    }
    while(h < 1 || h > 8);

    //Actually builds the pyramid
    for (int i = 1; i <= h; i++)
    {
        int num_hashes = i, num_spaces = w - num_hashes;
        repeat(' ', num_spaces);
        repeat('#', num_hashes);
        printf("  ");
        repeat('#', num_hashes);
        printf("\n");
    }
}
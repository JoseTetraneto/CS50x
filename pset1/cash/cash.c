#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main()
{
    int change;
    do
    {
        float dollars = get_float("Change owed: ");
        change = round(dollars * 100);
    }
    while (change <= 0);

    int q = 25, d = 10, n = 5, p = 1, coin_counter = 0;

    while (change >= q)
    {
        change -= q;
        coin_counter++;
    }
    while (change >= d)
    {
        change -= d;
        coin_counter++;
    }
    while (change >= n)
    {
        change -= n;
        coin_counter++;
    }
    while (change >= p)
    {
        change -= p;
        coin_counter++;
    }
    printf("%i\n", coin_counter);
}
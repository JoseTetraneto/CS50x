//Returns the libraries needed for the program
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//Runs the main program
int main(int argc, string argv[])
{
    //Checks if there is exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //Checks to make sure that each character of that command-line argument is a decimal digit
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    //Converts the key string to an actual integer
    int key = atoi(argv[1]);

    //Prompts user for message and print it
    string plain_text = get_string("What is your message? ");

    printf("plaintext: %s\n", plain_text);

    //Enciphers the plain_text and print the result
    printf("ciphertext: ");

    for (int i = 0, n = strlen(plain_text); i < n; i++)
    {
        if (isalpha(plain_text[i]) != 0)
        {
            if (isupper(plain_text[i]) != 0)
            {
                printf("%c", (((plain_text[i] + 26 - key) - 65) % 26) + 65);
            }
            else
            {
                printf("%c", (((plain_text[i] + 26 - key) - 97) % 26) + 97);
            }
        }
        else
        {
            printf("%c", plain_text[i]);
        }
    }
    printf("\n");
    return 0;
}
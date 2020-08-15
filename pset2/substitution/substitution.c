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
        printf("Usage: ./caesar KEY\n");
        return 1;
    }

    //Checks to make sure that command-line argument is 26 chars long, that it only contains letters and that it doesn't contain repetitive chars
    int p = -1;
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (strlen(argv[1]) != 26)
        {
            printf("KEY must contain 26 characters\n");
            return 1;
        }
        if (isdigit(argv[1][i]) != 0)
        {
            printf("KEY must contain only letters and no numbers\n");
            return 1;
        }
        if (isblank(argv[1][i]) != 0)
        {
            printf("KEY must contain only letters and no spaces\n");
            return 1;
        }
        for (int j = i + 1; j < n; j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                printf("KEY must not contain repetitive characters\n");
                return 1;
            }
        }
    }
    //Returns the key
    string key = argv[1];

    //Prompts user for message and print it
    string plain_text = get_string("What is your message? ");
    printf("plaintext: %s\n", plain_text);

    //Enciphers the plain_text and print the result
    printf("ciphertext: ");

    // Define array to collect keys characters.
    int arrayKeys[91];
    int index = 0;

    // Append the keys characters to the array.
    for (int i = 65; i <= 90; i++)
    {
        arrayKeys[i] = (int) toupper(key[index]);
        index++;
    }

    char charsArray[strlen(plain_text)];

    for (int i = 0, n = strlen(plain_text); i < n; i++)
    {
        if (islower(plain_text[i]))
        {
            charsArray[i] = (char) tolower(arrayKeys[((int) plain_text[i] - 32)]);
            printf("%c", charsArray[i]);
        }
        else if (isupper(plain_text[i]))
        {
            charsArray[i] = (char) arrayKeys[(int) plain_text[i]];
            printf("%c", charsArray[i]);
        }
        else
        {
            charsArray[i] = plain_text[i];
            printf("%c", charsArray[i]);
        }
    }
    printf("\n");
    return 0;
}
//Import the libraries needed
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

//Declare my functions
int count_letters(string t);
int count_words(string t);
int count_sentences(string t);
float index(int l, int w, int s);

//Runs the main program
int main(void)
{
    string text = get_string("input text: ");
    float i = index(count_letters(text), count_words(text), count_sentences(text));

    if (i < 16 && i >= 1)
    {
        printf("Grade %i\n", (int) round(i));
    }
    else if (i >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Before Grade 1\n");
    }

    return 0;
}

//Creates function to count the amount of letters
int count_letters(string t)
{
    int letters_count = 0;

    for (int i = 0; i < strlen(t); i++)
    {
        if (islower(t[i]) != 0 || isupper(t[i]) != 0)
        {
            letters_count++;
        }
        else
        {
            continue;
        }
    }
    return letters_count;
}

//Creates function to count the amount of words
int count_words(string t)
{
    int words_count = 0;

    for (int i = 0; i < strlen(t); i++)
    {
        if (isblank(t[i]) != 0)
        {
            words_count++;
        }
    }
    return words_count + 1;
}

//Creates function to count the amount of sentences
int count_sentences(string t)
{
    int sentences_count = 0;

    for (int i = 0; i < strlen(t); i++)
    {
        if (t[i] == '.' || t[i] == '!' || t[i] == '?')
        {

            sentences_count++;
        }
    }
    return sentences_count;
}

//Creates function to return Coleman-Liau index
float index(int l, int w, int s)
{
    float a = 100 / (float) w;
    float index = 0.0588 * ((float) l * a) - 0.296 * ((float) s * a) - 15.8;
    return index;
}
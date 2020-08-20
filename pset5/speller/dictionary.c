// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 50;

// Initialize number of words in hash table
unsigned int word_count;

// Hash table
node *table[N];


//----------------------------------------------------------------------------------------------------------------


// Loads dictionary into memory, returning true if successful else false --> Line 40 of speller.c
bool load(const char *dictionary)
{
    //Open the file
    //Use fopen to open file
    FILE *dict_ptr = fopen(dictionary, "r");

    //Check if return is NULL, and if so then print "error loading dictionary"
    if (dict_ptr == NULL)
    {
        printf("Error loading %s.\n", dictionary);
        return false;
    }

    //Read strings from file
    char buffer[LENGTH + 1];

    //Use fscanf(file pointer, "%s", char* word) in loop to get each word from the file (fscanf will return EOF once it reaches end of file)
    while (fscanf(dict_ptr, "%s", buffer) != EOF)
    {
        //Create a new node
        //Use malloc to allocate enough memory to store a new node (check if there's enough memory)
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Not enough memory to store dictionary!\n");
            fclose(dict_ptr);
            return false;
        }

        //Copy word into node using strcpy
        strcpy(n->word, buffer);

        //Hash Word
        //Call the hash function to determine which index into the hash table you should use when inserting the new node
        int index = hash(n->word);

        if (table[index] == NULL)
        {
            //Set head to new pointer
            table[index] = n;
        }
        else
        {
            //Set new pointer
            n->next = table[index];
        }
        //Increase word count to keep track of how many words have been processed
        word_count++;
    }
    //After loops endend, close file
    fclose(dict_ptr);

    //Return true as long as everything went fine
    return true;
}

// Hashes word to a number --> Line 68 of speller.c
unsigned int hash(const char *word)
{
    int sum = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        sum += tolower(word[i]);
    }
    sum *= tolower(word[0]);
    return (sum % N);
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded --> Line 144 of speller.c
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary else false --> Line 112 of speller.c
bool check(const char *word)
{
    //Hash word to get the index
    int index = hash(word);

    //Access the linked list at that index and traverse it looking for the word (use strcasecmp to compare case insensitive)
    node *pointer = table[index];
    while (pointer != NULL)
    {
        if (strcasecmp(pointer->word, word) == 0)
        {
            return true;
        }
        else
        {
            pointer = pointer->next;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false --> Line 152 of speller.c
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            free(temp);
            cursor = cursor->next;
        }
    }
    return true;
}

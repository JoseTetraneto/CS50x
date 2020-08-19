#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    //Checks if there is exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover file_to_recover\n");
        return 1;
    }

    //Open memory card
    FILE *mcptr = fopen(argv[1], "r");
    if (mcptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 1;
    }

    //Allocate memory for buffer
    uint8_t *buffer = malloc(512 * sizeof(uint8_t));
    if (buffer == NULL)
    {
        fprintf(stderr, "Not enough memory to store image.\n");
        fclose(mcptr);
        return 1;
    }

    FILE *img = NULL;
    int jpeg_count = 0;
    char jpeg_file[8];

    //Read memory card contents into buffer until the end of the last 512 byte block
    while (fread(buffer, sizeof(buffer), 1, mcptr) == 1)
    {
        //Look for beggining of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpeg_count > 0)
            {
                fclose(img);
            }

            //Creates a JPEG file
            sprintf(jpeg_file, "%03i.jpg", jpeg_count);

            //Open JPEG file in write mode
            img = fopen(jpeg_file, "w");

            // Write new pixels to image
            fwrite(buffer, sizeof(buffer), 1, img);

            jpeg_count++;
        }
        else if (jpeg_count > 0)
        {
            fwrite(buffer, sizeof(buffer), 1, img);
        }
    }
    //Free memory from buffer
    free(buffer);

    //Close memory card file
    fclose(mcptr);

    //Close JPEG file
    fclose(img);
}

#include <math.h>
#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int avg;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE *ptr = &image[i][j];
            avg = round(((*ptr).rgbtBlue + (*ptr).rgbtGreen + (*ptr).rgbtRed) / 3.0);
            (*ptr).rgbtBlue = (int) avg;
            (*ptr).rgbtGreen = (int) avg;
            (*ptr).rgbtRed = (int) avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE *ptr = &image[i][j];
            int sepiaRed = round(0.189 * (*ptr).rgbtBlue + 0.769 * (*ptr).rgbtGreen + 0.393 * (*ptr).rgbtRed);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            int sepiaGreen = round(0.168 * (*ptr).rgbtBlue + 0.686 * (*ptr).rgbtGreen + 0.349 * (*ptr).rgbtRed);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            int sepiaBlue = round(0.131 * (*ptr).rgbtBlue + 0.534 * (*ptr).rgbtGreen + 0.272 * (*ptr).rgbtRed);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            (*ptr).rgbtBlue = sepiaBlue;
            (*ptr).rgbtGreen = sepiaGreen;
            (*ptr).rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            tmp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Make a copy of the image
    RGBTRIPLE ptr[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ptr[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        //For every ptr...
        for (int j = 0; j < width; j++)
        {
            int counter = 0, red = 0, green = 0, blue = 0;
            //Current ptr
            red += ptr[i][j].rgbtRed;
            green += ptr[i][j].rgbtGreen;
            blue += ptr[i][j].rgbtBlue;
            counter++;

            //Check if ptr above and to the left exists
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red += ptr[i - 1][j - 1].rgbtRed;
                green += ptr[i - 1][j - 1].rgbtGreen;
                blue += ptr[i - 1][j - 1].rgbtBlue;
                counter++;
            }
            //ptr directly above
            if (i - 1 >= 0 && j >= 0)
            {
                red += ptr[i - 1][j].rgbtRed;
                green += ptr[i - 1][j].rgbtGreen;
                blue += ptr[i - 1][j].rgbtBlue;
                counter++;
            }
            //ptr above and to the right
            if (i - 1 >= 0 && j + 1 < width)
            {
                red += ptr[i - 1][j + 1].rgbtRed;
                green += ptr[i - 1][j + 1].rgbtGreen;
                blue += ptr[i - 1][j + 1].rgbtBlue;
                counter++;
            }
            //ptr to the left
            if (j - 1 >= 0)
            {
                red += ptr[i][j - 1].rgbtRed;
                green += ptr[i][j - 1].rgbtGreen;
                blue += ptr[i][j - 1].rgbtBlue;
                counter++;
            }
            //ptr to the right
            if (j + 1 < width)
            {
                red += ptr[i][j + 1].rgbtRed;
                green += ptr[i][j + 1].rgbtGreen;
                blue += ptr[i][j + 1].rgbtBlue;
                counter++;
            }
            //ptr below and to the left
            if (i + 1 < height && j - 1 >= 0)
            {
                red += ptr[i + 1][j - 1].rgbtRed;
                green += ptr[i + 1][j - 1].rgbtGreen;
                blue += ptr[i + 1][j - 1].rgbtBlue;
                counter++;
            }
            //ptr directly below
            if (i + 1 < height && j >= 0)
            {
                red += ptr[i + 1][j].rgbtRed;
                green += ptr[i + 1][j].rgbtGreen;
                blue += ptr[i + 1][j].rgbtBlue;
                counter++;
            }
            //ptr below and to the right
            if (i + 1 < height && j + 1 < width)
            {
                red += ptr[i + 1][j + 1].rgbtRed;
                green += ptr[i + 1][j + 1].rgbtGreen;
                blue += ptr[i + 1][j + 1].rgbtBlue;
                counter++;
            }

            image[i][j].rgbtRed = round(red / (counter * 1.0));
            image[i][j].rgbtGreen = round(green / (counter * 1.0));
            image[i][j].rgbtBlue = round(blue / (counter * 1.0));
        }
    }
    return;
}
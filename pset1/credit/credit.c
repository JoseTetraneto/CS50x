#include <cs50.h>
#include <stdio.h>

int main()
{
    long long card = get_long_long("Please input the Credit Card number: ");
    int last_digit = 0, second_last_digit = 0, num_digits = 0, sum_of_doubled_evens = 0, sum_of_odds = 0;

    while (card > 0)
    {
        second_last_digit = last_digit;
        last_digit = card % 10;

        if (num_digits % 2 == 0)
        {
            sum_of_odds += last_digit;
        }
        else
        {
            int multiple = 2 * last_digit;
            sum_of_doubled_evens += (multiple / 10) + (multiple % 10);
        }

        card /= 10;
        num_digits++;
    }

    bool is_valid = (sum_of_odds + sum_of_doubled_evens) % 10 == 0;
    int first_two_digits = (last_digit * 10) + second_last_digit;

    if (last_digit == 4 && num_digits >= 13 && num_digits <= 16 && is_valid)
    {
        printf("VISA\n");
    }
    else if (first_two_digits >= 51 && first_two_digits <= 55 && num_digits == 16 && is_valid)
    {
        printf("MASTERCARD\n");
    }
    else if ((first_two_digits == 34 || first_two_digits == 37) && num_digits == 15 && is_valid)
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
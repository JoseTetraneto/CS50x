from cs50 import get_int

card = get_int('Please input the Credit Card number: ')
last_digit, second_last_digit, num_digits, sum_of_doubled_evens, sum_of_odds = 0, 0, 0, 0, 0

while card > 0:
    second_last_digit = last_digit
    last_digit = int(card % 10)

    if num_digits % 2 is 0:
        sum_of_odds += last_digit
    else:
        multiple = 2 * last_digit
        sum_of_doubled_evens += int((multiple / 10)) + int((multiple % 10))

    card = int(card/10)
    num_digits += 1

is_valid = (sum_of_odds + sum_of_doubled_evens) % 10 == 0
first_two_digits = (last_digit * 10) + second_last_digit

if last_digit == 4 and num_digits >= 13 and num_digits <= 16 and is_valid:
    print('VISA')

elif first_two_digits >= 51 and first_two_digits <= 55 and num_digits == 16 and is_valid:
    print('MASTERCARD')

elif (first_two_digits == 34 or first_two_digits == 37) and num_digits == 15 and is_valid:
    print('AMEX')

else:
    print('INVALID')
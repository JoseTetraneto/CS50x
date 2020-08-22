from cs50 import get_float

amount = get_float('How much is owed?\n')
while amount <= 0:
    amount = get_float('Must be a positive value\n')

change = amount * 100

q, d, n, p = 25, 10, 5, 1

coins = int(change/q) + int((change % q)/d) + int(((change % q) % d)/n) + int((((change % q) % d) % n)/p)

print(coins)
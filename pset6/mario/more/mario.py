from cs50 import get_int

height = get_int('What is the height of the pyramid?\n')

while height < 1 or height > 8:
    height = get_int('Height must be from 1 to 8!\n')

c = 1
for i in range(height):
    for j in range(height):
        if i + j < height - 1:
            print(' ', end='')
        else:
            print('#', end='')
    print('  ', end='')
    print('#' * c, end='')
    c += 1
    print()
from cs50 import get_int

height = get_int('What is the height of the pyramid?\n')

while height < 0 or height > 8:
    height = get_int('Height must be from 0 to 8!\n')

for i in range(height):
    for j in range(height):
        if i + j < height - 1:
            print(' ', end='')
        else:
            print('#', end='')
    print()
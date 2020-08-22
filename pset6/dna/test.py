from sys import argv, exit

if len(argv) != 2:
    print("missing command-line argument")
    exit()
print(f"hello, {argv[1]}")
exit()
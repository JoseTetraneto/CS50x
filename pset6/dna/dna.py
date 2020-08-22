import csv
from sys import argv, exit

# Ensures only 3 command-line arguments

if len(argv) != 3:
    print('Usage: python dna.py database.csv sequence.txt')
    exit(1)

# Opens the database.csv and reads it into memory

with open(argv[1], 'r') as database:
    reader_data = csv.reader(database)
    data = list(reader_data)

# Converts 'numebr strings' into actual numbers

for i in range(1, len(data)):
    for j in range(1, len(data[i])):
        data[i][j] = int(data[i][j])

# Opens the sequence.txt and reads it into memory

with open(argv[2], 'r') as sequence:
    reader_seq = csv.reader(sequence)
    seq = list(reader_seq)

# Iterate over the sequence and return results in a list

counter, j = 0, 0
data1 = data[0][1:]
seq1 = seq[0][0]
results = []

for i in range(len(data1)):
    counter = 0
    occurrences = []
    j = 0

    while j < len(seq1):
        if seq1[j:j + len(data1[i])] == data1[i]:
            counter += 1
            j += len(data1[i])
        else:
            if counter > 0:
                occurrences.append(counter)
            counter = 0
            j += 1
    if len(occurrences) > 0:
        occurrences.sort()
        results.append(occurrences[-1])

# Compares the results obtained with the database to identify the person

for i in range(1, len(data)-1):
    if results == data[i][1:]:
        print(data[i][0])
        exit(0)
print('No match')
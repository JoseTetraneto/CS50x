import cs50
import csv
from csv import reader
from sys import argv, exit

# Ensures only 3 command-line arguments

if len(argv) != 2:
    print('Usage: python import.py database.csv')
    exit(1)

# Creates database if it hasn`t been already, else just open and close it (in 'w' mode to promote overwrites)

open("students.db", "w").close()
db = cs50.SQL("sqlite:///students.db")

# Creates a table within the database

db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

# Opens .csv file, reads it, splits the names, converts births to integers and adds everything to the database

with open(argv[1], newline='') as csv_file:
    file = reader(csv_file)
    for row in file:
        if row[0] == "name":
            continue
        name = row[0].split()

        if len(name) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], name[1], name[2], row[1], row[2])
        else:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], None, name[1], row[1], row[2])
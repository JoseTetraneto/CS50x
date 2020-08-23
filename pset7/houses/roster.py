import cs50
from sys import argv, exit

# Ensures only 3 command-line arguments

if len(argv) != 2:
    print('Usage: python roster.py <house>')
    exit(1)

# Connects to database
db = cs50.SQL("sqlite:///students.db")

# Fetches Roaster
roaster = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", argv[1])

# Prints Roaster
for row in roaster:
    if row["middle"] is None:
        name = row["first"] + " " + row["last"]
    else:
        name = row["first"] + " " + row["middle"] + " " + row["last"]

    print(f"{name}, born {row['birth']}")
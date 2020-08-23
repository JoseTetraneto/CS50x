import cs50
from sys import argv, exit

# Ensures only 3 command-line arguments

if len(argv) != 2:
    print('Usage: python roster.py <house>')
    exit(1)

# Connects to database
db = cs50.SQL("sqlite:///students.db")

# Fetches Roaster
roaster = db.execute("SELECT * FROM students WHERE House = ? ORDER BY Last_Name, First_Name", argv[1])

# Prints Roaster
for row in roaster:
    if row["middle"] is None:
        name = row["First_Name"] + " " + row["Last_Name"]
    else:
        name = row["First_Name"] + " " + row["Middle_Name"] + " " + row["Last_Name"]

    print(f"{name}, born {row['Birth']}")
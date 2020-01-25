import csv

with open("inputFile1.csv") as csvfile:
    lines = csv.reader(csvfile)
    print(next(lines))

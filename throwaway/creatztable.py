"""Throwaway code, used to create z_table dictionary"""

# TODO: create the data structure to contain the probabilities
# TODO: import the excel file containing the table
# TODO: Open the python file containing the table
# TODO: loop through the table, adding each probability to the structure
# TODO: Close everything

import csv

with open("studentT.py", "a") as append_file:
    with open("studentT.csv", "r") as read_file:
        # Assign csv file object to a csv.reader object
        csvReader = csv.reader(read_file)
        # Skip first row
        next(csvReader)
        key = 0.00
        for row in csvReader:
            for column in row[1:]:
                # append_file.write(f"        {0 - round(key, 2)}: {round(1 - float(column), 4)},\n")
                print(f"    {0 - round(key, 2)}: {round(1 - float(column), 4)},\n")
                key += 0.01

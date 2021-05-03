"""Throwaway code, used to create T_table dictionary"""

import csv

with open("studentT.py", "a") as append_file:
    with open("studentT.csv", "r") as read_file:
        # Assign csv file object to a csv.reader object
        csvReader = csv.reader(read_file)
        key = 0
        sub_keys = []
        row_counter = 0
        for row in csvReader:
            temp_row_string = ""
            if row_counter == 0:
                sub_keys = row[1:]
                print(f"sub_keys = {sub_keys}")
                row_counter += 1
            else:
                key = row[0]
                for i in range(len(row[1:])):
                    temp_row_string += f"{sub_keys[i]}: {row[i+1]}, "
            temp_row_string = f"{' '*16}{key}: {{{temp_row_string[:-2]}}}, \n"
            append_file.write(temp_row_string)

'''
                {0.1: 3.078, 0.05: 6.314, 0.025: 12.706, 0.01: 31.821, 0.005: 63.657}
'''


            #     values = []
            #     if row_counter == 0:
            #         sub_keys.append(column)
            #         print(sub_keys)
            #         row_counter += 1
            #     else:
            #         column_counter = 0
            #         if column_counter == 0:
            #             key = column
            #             column_counter += 1
            #         else:
            #             values.append(column)
            # for sub_key, value in range(len(sub_keys)):
            #     temp_write_string += f"{sub_key}: {value}, "
            # temp_write_string = temp_write_string[:-2] + "}, \n"
            #
            # print(temp_write_string)


# append_file.write(f"        {0 - round(key, 2)}: {round(1 - float(column), 4)},\n")
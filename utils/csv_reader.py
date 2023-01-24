# PYTHON VERSION

import csv_reader

def read_record(row):
    # File pointer
    fin = open("../curva_reflow.csv", "r")

    a = [25, 38, 46, 54, 57, 61, 63, 54, 33, 25]
    if not fin.readable():
        for i in range(10):
            row.time[i] = a[i]
            row.temp[i] = a[i]
        return

    # Read the Data from the file
    count = 0
    for line in fin:
        if count == 0:
            count += 1
            continue
        data = line.strip().split(",")
        row.time[count-1] = int(data[0])
        row.temp[count-1] = int(data[1])
        count += 1
    if count == 1:
        print("Record not found")
    fin.close()
    return
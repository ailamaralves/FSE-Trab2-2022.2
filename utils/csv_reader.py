class Row:
    temp = []
    time = []

def read_record():
    fin = open("../curva_reflow.csv", "r")
    row = Row()
    a = [25, 38, 46, 54, 57, 61, 63, 54, 33, 25]
    if not fin.readable():
        for i in range(10):
            row.time[i] = a[i]
            row.temp[i] = a[i]
        return

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
    return row


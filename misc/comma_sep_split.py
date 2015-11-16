"""for expanding out and copying rows where a cell has a delimeted list
    ie: A | B | 1,2,3 becomes:
        A | B | 1
        A | B | 2
        A | B | 3"""

import csv

CSV_LOC = "/Users/ewanog/Documents/nepal/Shelter/Winterisation Survey.csv"
SPLIT_NAME = 'district'
SPLIT_VAL = ','

def ingest_csv():
    """read in csv and convert to dict"""
    with open(CSV_LOC, 'rb') as f:
        reader = csv.reader(f)
        return list(reader)


def get_new_rows(row,ind):
    new_rows = []
    for v in row[ind].split(SPLIT_VAL):
        new_rows.append(row[:ind] + [v] + row[ind+1:] + [row[ind], len(row[ind].split(SPLIT_VAL))])

    return new_rows

def split(vals):
    """go through row and split entries"""
    try:
        ind = vals[0].index(SPLIT_NAME)
    except:
        print 'cant find lookup!'

    output = [vals[0] + ['original', 'count']]

    for row in vals[1:]:
        if SPLIT_VAL in row[ind]:
            for r in get_new_rows(row, ind):
                output.append(r)
        else:
            output.append(row + [row[ind], '1'])

    return output

def write_out(out):
    f = open(CSV_LOC.replace('.csv','') + '_split.csv', 'wt')
    writer = csv.writer(f)
    for row in out:
        print row
        if row is not None:
            writer.writerow(row)




    f.close()


if __name__ == '__main__':
    vals = ingest_csv()
    out = split(vals)
    write_out(out)
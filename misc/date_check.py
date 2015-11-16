import openpyxl
import etl
from datetime import datetime
import csv

s = etl.pull_wb('/Users/ewanog/Documents/tmp/date_test.xlsx', 'local', True).active

for r in s.rows[1:]:
    for v in r:
        rv = v.value
        if rv is not None:
            first = int(rv.split('/')[0])
            second = int(rv.split('/')[1])
            third = int(rv.split('/')[2])

            if third in [15,16,17]:
                third = '20' + str(third)

            if second < 4 and first < 25:
                t = first
                first = second
                second = t

            v.value = str(first) + "/"  + str(second) + "/" + str(third)

            try:
                v.value = etl.convert_date(v.value, '%d/%m/%Y', '%d/%m/%Y')
            except:
                try:
                    v.value = etl.convert_date(v.value, '%d/%m/%y', '%d/%m/%Y')
                except:
                    try:
                        v.value = etl.convert_date(v.value, '%m/%d/%y', '%d/%m/%Y')
                    except:
                        try:
                            v.value = etl.convert_date(v.value, '%m/%d/%Y', '%d/%m/%Y')
                        except:
                            'cant parse: ' + v.value

with open('/Users/ewanog/Documents/tmp/dates.csv', 'w') as f:
    csv_out = csv.writer(f, delimiter=',')
    csv_out.writerow(etl.get_values(s.rows[0]))
    for r in s.rows[1:]:
        out = []
        for v in r:
            try:
                if v.value is not None:
                    out.append(v.value)
            except Exception, e:
                print e

        csv_out.writerow(out)
        print str(out)

    f.close()

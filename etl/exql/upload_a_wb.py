"""read in a workbook and upload it to SQL"""
from openpyxl import Workbook

import etl
import master_db_creation
from sqlalchemy import Column, Integer, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.cell import column_index_from_string
import click
import os
import re
import sh_obj
import psycopg2

engine = create_engine(os.environ['dbk'])
m = MetaData()
m.reflect(engine)

conn = psycopg2.connect(os.environ['dbk'])
cur = conn.cursor()


def append_sht(sht, tbl_nm, col_nms):
    """append ws values to a table"""
    cur = conn.cursor()

    fmt = ','.join(['%s'] * len(sht.values))
    insert_query = 'insert into {0} {1} values {2}'.format(tbl_nm, sht.col_nms, fmt)
    cur.execute(insert_query, sht.values)
    cur.commit()

def create_with_sheet(sht, tbl_nm):
    """insert ws into a new table"""
    cur = conn.cursor()

    ctable = get_pg_create(sht.col_nms)

def get_pg_create(col_nms)

    cur.execute("CREATE TABLE ")

@click.command()
@click.option('--src', help='local files or on dropbox?', type = click.Choice(['db','local']))
@click.option('--sheet_name', help='which sheet should we pull?')
@click.option('--path', help='file path to xlsx or directory')
@click.option('--test', help='are we testing?', is_flag = True)
@click.option('--append', help='we are appending?', is_flag = True)
@click.option('--table_name', help='name of table appending or creating to')
@click.option('--col_names', help='optional, list of column names. defaults to header', required=False)


def ingest(src, path, test, sht_n, append, tbl_nm, col_nms):
    """iterate through wbs and send to sql"""

    sht_raw = etl.pull_wb(src, path, sheet_name).get_sheet_by_name(sheet_name)
    sht = sh_obj(sht_raw, path)

    if tbl_nm not in [t for t in m.tables.values() & append]:
        raise Exception('table does not exist to append to')

    elif append:
        append_sht(sht, tbl_nm)

    elif not append:
        create_with_sheet(sht, tbl_nm)


#Do we want to have option for multiple wbs? how to handle that logic? this would be
#better in utils file i think
def import_wbs(src, path, sheet_name):
    """decide if we're returning either a single or list of workbook objects"""

    wbs = []
    if os.path.isfile(path):
        try:
            wbs = etl.pull_wb(path, src)
        except:
            Exception('Cant pull this workbook!')

    else:
        #read in WS by WS and note any invalid notebooks. if we find >=1, Exception

        file_list = etl.get_file_list(path, src)
        bad_wb = []

        for f in file_list:
            try:
                wbs.append[etl.pull_wb(path, src)]
            except:
                bad_wb.append(path)

        if len(bad_wb) > 0:
            Exception('Workbook directory has an invalid workbook!' + path)

    return get_sheets(wbs, sheet_name)

def get_sheets(wbs, sheet_name):
    """return specified worksheets from given wbs"""
    ws = []

    for wb in wbs:
        for s in wb.worksheets:
            if s.title in sheet_name:
                ws.append(s)

    return ws

if __name__ == '__main__':
    wb = ingest()
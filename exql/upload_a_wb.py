"""read in a workbook and upload it to SQL"""
from openpyxl import Workbook

import etl
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
import Sheet

conn = None
engine = None


def get_conn():
    return create_engine(os.environ['dbk'])
    #m = MetaData()
    #m.reflect(engine)


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


def get_sht_nm(wb, sht_nm):
    """decide which sheet to pull from wb (default to first if None)"""
    if sht_nm == None:
        return wb.sheetnames[0]
    else:
        return sht_nm


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

def create_with_sheet(sht, tbl_nm):
    """create a SQL table and populate with data"""
    print sht.col_nms


@click.command()
@click.option('--src', help='local files or on dropbox?', type = click.Choice(['db','local']))
@click.option('--sheet_name', help='which sheet should we pull? Defaults to first if blank')
@click.option('--path', help='file path to xlsx or directory')
@click.option('--test', help='are we testing?', is_flag = True)
@click.option('--append', help='we are appending to SQL table or insterting?', is_flag = True)
@click.option('--table_name', help='name of table appending or creating to')
@click.option('--col_names', help='optional, list of column names in SQL table. defaults to header', required=False)
def ingest(src, path, test, sht_nm, append, tbl_nm, col_nms, sheet_name):
    """iterate through wbs and send to sql"""

    wb = etl.pull_wb(src, path, True)
    sht_raw = wb.get_sheet_by_name(get_sht_nm(wb, sht_nm))
    sht = Sheet(sht_raw, sheet_name)

    if not engine.has_key(tbl_nm) & append:
        raise Exception('Table does not exist to append to')

    elif append:
        append_sht(sht, tbl_nm)

    elif not append:
        create_with_sheet(sht, tbl_nm)

if __name__ == '__main__':
    global engine
    engine = get_conn()
    ingest()


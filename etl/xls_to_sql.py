"""take sheet(s) from an xls and return a SQLA object to be uploaded"""
#TODO: custom column names
#sepcify columns

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
import re
import os

@click.command()
@click.option('--src', help='local files or on dropbox?', type = click.Choice(['db','local']))
@click.option('--sheet_name', help='which sheets should we pull? (list)')
@click.option('--path', help='file path to xlsx or directory')
@click.option('--test', help='are we testing?', is_flag = True)
@click.option('--append', help='we are appending?', is_flag = True)
@click.option('--table_name', help='name of table appending or creating to')

engine = create_engine(os.environ['dbk'])
m = MetaData()
m.reflect(engine)


def append_sheets(wbs, tn):



def convert(src, path, test, sheet_name, append, table_name):
    """iterate through wbs and send to sql"""

    wbs = import_wbs(src, path, sheet_name)

    if append:
        if table_name not in [t for t in m.tables.values()]:
            raise Exception('table does not exist to append to ')
        else:
            append_sheets(wbs)
    else:
        for wb in wbs:
            create_table(wb, table_name)


def import_wbs(src, path, sheet_name):
    """decide if we're returning either a single or list of worksheet objects"""
    wbs = []
    if re.search('xls|xlsx$',str(path)):
        wbs = etl.pull_wb(path, src)
    else:
        file_list = etl.get_file_list(path, src)
        for f in file_list:
            wbs.append[etl.pull_wb(path, src)]

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
    convert()
"""take sheet(s) from an xls and return an array of SQL upload objects"""
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
@click.command()
@click.option('--src', help='local files or on dropbox?', type = click.Choice(['db','local']))
@click.option('--sheet_name', help='which sheets should we pull? (list)')
@click.option('--path', help='file path to xlsx or directory')
@click.option('--test', help='are we testing?', is_flag = True)
@click.option('--append', help='we are appending?', is_flag = True)
@click.option('--table_name', help='name of table appending or creating to')


import os
engine = create_engine(os.environ['dbk'])
m = MetaData()
m.reflect(engine)
import re




def append_sheets(wbs, tn):




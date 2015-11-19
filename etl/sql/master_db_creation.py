"""read in master db file and upload it to SQL"""
#TODO: read in DDL from xls or somethign better

from sqlalchemy import create_engine

import os
import sys
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import click
import dropbox
from etl import etl
from openpyxl.cell import column_index_from_string


#SQLA
engine = create_engine(os.environ['dbk'])
Base = declarative_base(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#dbox
db_access = os.environ['db_access']
client = dropbox.client.DropboxClient(db_access)

class Distributions(Base):
    """create table"""

    """
    Priority : priority
    Hard to Reach Access Methods : access_method
    Shelter Cluster Hub : hub
    Last Update	: as_of
    District HLCIT  Code : dist_code
    VDC / Municipality HLCIT  Code : vdc_code
    UNOCHA Activity Categories : act_cat

    Implementing agency	:	imp_agency
    Sourcing Agency	:	source_agency
    Local partner agency	:	local_partner
    Contact Name	:	contact_name
    Contact Email	:	contact_email
    Contact Phone Number	:	contact_phone

    District	:	district
    VDC / Municipalities	:	vdc
    Municipal Ward	:	ward

    Action type	:	act_type
    Action description	:	act_desc
    Targeting	:	targeting
    # Items / # Man-hours / NPR	:	quantity
    Total Number Households	:	total_hh
    Average cost per households (NPR)	:	avg_hh_cost
    Female headed households	:	fem_hh
    Vulnerable Caste / Ethnicity households 	:	vuln_hh

    Activity Status	:	act_status
    "Start date (Actual or Planned)"	:	start_dt
    start_day : start_day
    start_month : start_month
    start_year : start_year
    "Completion Date (Actual or Planned)"	:	comp_dt
    comp_day : comp_day
    comp_month : comp_month
    comp_year : comp_year
    Additional Comments	:	comments
    """

    __tablename__ = 'distributions'

    priority = Column(String)
    access_method = Column(String)
    hub = Column(String)
    as_of = Column(String)
    dist_code = Column(String)
    vdc_code = Column(String)
    act_cat = Column(String)

    imp_agency = Column(String)
    source_agency = Column(String)
    local_partner = Column(String)
    contact_name = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)

    district = Column(String)
    vdc = Column(String)
    ward = Column(String)

    act_type = Column(String)
    act_desc = Column(String)
    targeting = Column(String)
    quantity = Column(Float)
    total_hh = Column(Float)
    avg_hh_cost = Column(Float)
    fem_hh = Column(Float)
    vuln_hh = Column(Float)

    act_status = Column(String)
    start_dt = Column(String)
    start_day = Column(Integer)
    start_month = Column(Integer)
    start_year = Column(Integer)
    comp_dt = Column(String)
    comp_day = Column(Integer)
    comp_month = Column(Integer)
    comp_year = Column(Integer)
    comments = Column(String)
    pk = Column(Integer, primary_key=True)

@click.command()
@click.option('--path', help = 'path to spreadsheet')
@click.option('--location', help = 'locaiton of spreadsheet (local or db)')
@click.option('--table_name', help = 'name of table to be created ')
def insert_data(path, location, table_name):
    """iterate over each row and add to db"""
    ws = etl.pull_wb(path, location, True).get_sheet_by_name('Distributions')
    locs = get_locs(ws)

    it=0
    for r in ws.rows[1:]:
        it+=1
        print 'row' + str(it)
        session.add(prep_row(r,locs))
        if it % 100 == 0:
            print 'commit'
            session.commit()

    #catch any leftover rows
    session.commit()


def prep_row(r, locs):
    #check to see if numeric rows are None - if so, make 0
    r = etl.get_values(r, setnull=True)

    return Distributions(
    priority=etl.xstr(r[locs["priority"]-1], setnull=True),
    access_method=etl.xstr(r[locs["access_method"]-1], setnull=True),
    hub=etl.xstr(r[locs["hub"]-1], setnull=True),
    as_of=etl.xstr(r[locs["as_of"]-1], setnull=True),
    dist_code=etl.xstr(r[locs["dist_code"]-1], setnull=True),
    vdc_code=etl.xstr(r[locs["vdc_code"]-1], setnull=True),
    act_cat=etl.xstr(r[locs["act_cat"]-1], setnull=True),

    imp_agency=etl.xstr(r[locs["imp_agency"]-1], setnull=True),
    source_agency=etl.xstr(r[locs["source_agency"]-1], setnull=True),
    local_partner=etl.xstr(r[locs["local_partner"]-1], setnull=True),
    contact_name=etl.xstr(r[locs["contact_name"]-1], setnull=True),
    contact_email=etl.xstr(r[locs["contact_email"]-1], setnull=True),
    contact_phone=etl.xstr(r[locs["contact_phone"]-1], setnull=True),

    district=etl.xstr(r[locs["district"]-1], setnull=True),
    vdc=etl.xstr(r[locs["vdc"]-1], setnull=True),
    ward=etl.xstr(r[locs["ward"]-1], setnull=True),

    act_type=etl.xstr(r[locs["act_type"]-1], setnull=True),
    act_desc=etl.xstr(r[locs["act_desc"]-1], setnull=True),
    targeting=etl.xstr(r[locs["targeting"]-1], setnull=True),
    quantity=etl.xstr(r[locs["quantity"]-1], setnull=True),
    total_hh=etl.xstr(r[locs["total_hh"]-1], setnull=True),
    avg_hh_cost=etl.xstr(r[locs["avg_hh_cost"]-1], setnull=True),
    fem_hh=etl.xstr(r[locs["fem_hh"]-1], setnull=True),
    vuln_hh=etl.xstr(r[locs["vuln_hh"]-1], setnull=True),

    act_status=etl.xstr(r[locs["act_status"]-1], setnull=True),
    start_dt=etl.xstr(r[locs["start_dt"]-1], setnull=True),
    start_day=etl.xstr(r[locs["start_day"]-1], setnull=True),
    start_month=etl.xstr(r[locs["start_month"]-1], setnull=True),
    start_year=etl.xstr(r[locs["start_year"]-1], setnull=True),
    comp_dt=etl.xstr(r[locs["comp_dt"]-1], setnull=True),
    comp_day=etl.xstr(r[locs["comp_day"]-1], setnull=True),
    comp_month=etl.xstr(r[locs["comp_month"]-1], setnull=True),
    comp_year=etl.xstr(r[locs["comp_year"]-1], setnull=True),
    comments=etl.xstr(r[locs["comments"]-1], setnull=True))
   # pk=gen_pk(r, locs))

def gen_pk(r, locs):
    return etl.xstr(r[locs["imp_agency"]-1].value)+etl.xstr(r[locs["local_partner"]-1].value)+etl.xstr(r[locs["district"]-1].value)+etl.xstr(r[locs["vdc"]-1].value)+etl.xstr(r[locs["ward"]-1].value)+etl.xstr(r[locs["act_type"]-1].value)+etl.xstr(r[locs["act_desc"]-1].value)+etl.xstr(r[locs["quantity"]-1].value)+etl.xstr(r[locs["total_hh"]-1].value)


def get_locs(ws):
    """find column headers in advance so we don't have to call each time"""
    ret = {}
    ret["priority"]=column_index_from_string(etl.find_in_header(ws,"Priority"))
    ret["access_method"]=column_index_from_string(etl.find_in_header(ws,"Hard to Reach Access Methods"))
    ret["hub"]=column_index_from_string(etl.find_in_header(ws,"Shelter Cluster Hub"))
    ret["as_of"]=column_index_from_string(etl.find_in_header(ws,"Last Update"))
    ret["dist_code"]=column_index_from_string(etl.find_in_header(ws,"District HLCIT Code"))
    ret["vdc_code"]=column_index_from_string(etl.find_in_header(ws,"VDC / Municipality HLCIT Code"))
    ret["act_cat"]=column_index_from_string(etl.find_in_header(ws,"UNOCHA Activity Categories"))

    ret["imp_agency"]=column_index_from_string(etl.find_in_header(ws,"Implementing agency"))
    ret["source_agency"]=column_index_from_string(etl.find_in_header(ws,"Sourcing Agency"))
    ret["local_partner"]=column_index_from_string(etl.find_in_header(ws,"Local partner agency"))
    ret["contact_name"]=column_index_from_string(etl.find_in_header(ws,"Agency / Local Contact Name"))
    ret["contact_email"]=column_index_from_string(etl.find_in_header(ws,"Agency / Local Contact Email"))
    ret["contact_phone"]=column_index_from_string(etl.find_in_header(ws,"Agency / Local Contact Phone #"))

    ret["district"]=column_index_from_string(etl.find_in_header(ws,"District"))
    ret["vdc"]=column_index_from_string(etl.find_in_header(ws,"VDC / Municipalities"))
    ret["ward"]=column_index_from_string(etl.find_in_header(ws,"Municipal Ward"))

    ret["act_type"]=column_index_from_string(etl.find_in_header(ws,"Action type"))
    ret["act_desc"]=column_index_from_string(etl.find_in_header(ws,"Action description"))
    ret["targeting"]=column_index_from_string(etl.find_in_header(ws,"Targeting"))
    ret["quantity"]=column_index_from_string(etl.find_in_header(ws,"# Items / # Man-hours / NPR"))
    ret["total_hh"]=column_index_from_string(etl.find_in_header(ws,"Total Number Households"))
    ret["avg_hh_cost"]=column_index_from_string(etl.find_in_header(ws,"Average cost per households (NPR)"))
    ret["fem_hh"]=column_index_from_string(etl.find_in_header(ws,"Female headed households"))
    ret["vuln_hh"]=column_index_from_string(etl.find_in_header(ws,"Vulnerable Caste / Ethnicity households"))

    ret["act_status"]=column_index_from_string(etl.find_in_header(ws,"Activity Status"))
    ret["start_dt"]=column_index_from_string(etl.find_in_header(ws,"Start date"))
    ret["start_day"]=column_index_from_string(etl.find_in_header(ws,"start_day"))
    ret["start_month"]=column_index_from_string(etl.find_in_header(ws,"start_month"))
    ret["start_year"]=column_index_from_string(etl.find_in_header(ws,"start_year"))
    ret["comp_dt"]=column_index_from_string(etl.find_in_header(ws,"Completion Date"))
    ret["comp_day"]=column_index_from_string(etl.find_in_header(ws,"comp_day"))
    ret["comp_month"]=column_index_from_string(etl.find_in_header(ws,"comp_month"))
    ret["comp_year"]=column_index_from_string(etl.find_in_header(ws,"comp_year"))
    ret["comments"]=column_index_from_string(etl.find_in_header(ws,"Additional Comments"))
    return ret

if __name__ == '__main__':
    if Base.metadata.tables.has_key('distributions'):
        Base.metadata.tables['distributions'].drop(engine, checkfirst = True)
    Base.metadata.create_all(engine)
    insert_data()
    print 'done'

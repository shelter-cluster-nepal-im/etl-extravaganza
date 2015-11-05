"""read in master db file and upload it to SQL"""
# TODO: read in DDL from xls or somethign better
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
import etl
from openpyxl.cell import column_index_from_string


# SQLA
engine = create_engine(os.environ['dbk'])
Base = declarative_base(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# dbox
db_access = os.environ['db_access']
client = dropbox.client.DropboxClient(db_access)


class Trainings(Base):
    """create table"""

    """
    Priority : priority
    Hard to Reach Access Methods : access_method
    Shelter Cluster Hub : hub
    Last Update	: as_of
    District HLCIT  Code : dist_code
    VDC / Municipality HLCIT  Code : vdc_code
    UID : uid

    Implementing agency	:	imp_agency
    Sourcing Agency	:	source_agency
    Local partner agency	:	local_partner
    Contact Name	:	contact_name
    Contact Email	:	contact_email
    Contact Phone Number	:	contact_phone

    District	:	district
    VDC / Municipalities	:	vdc
    Municipal Ward	:	ward

    Training Subject	: train_sub
    Audience	 : audience
    Training Title	:train_title
    Demonstration Construction Included?	: demo_inc
    IEC Materials Distributed	: iec_dist
    Duration of each session (hours)	: dur_session
    Amount Paid to Participants (NPR per participant)	: amt_parti
    Total Cost Per Training	: total_cost
    Total Participants (Individuals)	: total_parti
    Males	: males
    Females	: females
    Third Gender	:third_gen
    Elderly (60+)	: elderly
    Children (under 18)	: children
    Persons with Disabilities	:person_dis
    Vulnerable Caste or Ethnicity	: vuln_hh
    Female Headed Households (if applicable) : 	fem_hh

    Activity Status	:	act_status
    "Start date (Actual or Planned)"	:	start_dt
    "Completion Date (Actual or Planned)"	:	comp_dt

    Additional Comments	:	comments
    """

    __tablename__ = 'trainings'

    priority = Column(String)
    access_method = Column(String)
    hub = Column(String)
    as_of = Column(String)
    dist_code = Column(String)
    vdc_code = Column(String)
    uid = Column(String)

    imp_agency = Column(String)
    source_agency = Column(String)
    local_partner = Column(String)
    contact_name = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)

    district = Column(String)
    vdc = Column(String)
    ward = Column(String)

    train_sub = Column(String)
    audience = Column(String)
    train_title = Column(String)
    demo_inc = Column(String)
    iec_dist = Column(String)
    dur_session = Column(String)
    amt_parti = Column(Float)
    total_cost = Column(Float)
    total_parti = Column(Integer)
    males = Column(Integer)
    females = Column(Integer)
    third_gen = Column(Integer)
    elderly = Column(Integer)
    children = Column(Integer)
    person_dis = Column(Integer)
    vuln_hh = Column(Float)
    fem_hh = Column(Float)

    act_status = Column(String)
    start_dt = Column(String)
    comp_dt = Column(String)

    comments = Column(String)
    pk = Column(Integer, primary_key=True)


@click.command()
@click.option('--path', help='path to spreadsheet')
@click.option('--location', help='locaiton of spreadsheet (local or db)')
@click.option('--table_name', help='name of table to be created ')
def insert_data(path, location, table_name):
    """iterate over each row and add to db"""
    ws = etl.pull_wb(path, location, True).get_sheet_by_name('Trainings')
    locs = get_locs(ws)

    it = 0
    for r in ws.rows[1:]:
        it += 1
        print 'row' + str(it)
        session.add(prep_row(r, locs))
        if it % 100 == 0:
            print 'commit'
            session.commit()

    # catch any leftover rows
    session.commit()


def check_zero_entries(r, locs, meta):
    """iterate through each value and see if any ints are Nones, set to 0"""
    for col in meta.columns:
        if (isinstance(col.type, Integer) or isinstance(col.type, Float)) and col.description != 'pk' \
                and etl.xstr(r[locs[col.description] - 1].value) == 'None':
            r[locs[col.description] - 1].value = '0'

    return r


def make_null(r, locs, meta):
    """iterate through each value and see if any values are Nones, set to None (Null in db)"""
    for col in meta.columns:
        if col.description != 'pk' and etl.xstr(r[locs[col.description] - 1].value) == 'None':
            r[locs[col.description] - 1].value = None

    return r


def prep_row(r, locs):
    # check to see if numeric rows are None - if so, make 0
    r = etl.get_values(r, setnull=True)

    return Trainings(
    priority=etl.xstr(r[locs["priority"]-1], setnull=True),
    access_method=etl.xstr(r[locs["access_method"]-1], setnull=True),
    hub=etl.xstr(r[locs["hub"]-1], setnull=True),
    as_of=etl.xstr(r[locs["as_of"]-1], setnull=True),
    dist_code=etl.xstr(r[locs["dist_code"]-1], setnull=True),
    vdc_code=etl.xstr(r[locs["vdc_code"]-1], setnull=True),
    uid=etl.xstr(r[locs["uid"]-1], setnull=True),
    imp_agency=etl.xstr(r[locs["imp_agency"]-1], setnull=True),
    source_agency=etl.xstr(r[locs["source_agency"]-1], setnull=True),
    local_partner=etl.xstr(r[locs["local_partner"]-1], setnull=True),
    contact_name=etl.xstr(r[locs["contact_name"]-1], setnull=True),
    contact_email=etl.xstr(r[locs["contact_email"]-1], setnull=True),
    contact_phone=etl.xstr(r[locs["contact_phone"]-1], setnull=True),
    district=etl.xstr(r[locs["district"]-1], setnull=True),
    vdc=etl.xstr(r[locs["vdc"]-1], setnull=True),
    ward=etl.xstr(r[locs["ward"]-1], setnull=True),
    train_sub=etl.xstr(r[locs["act_type"]-1], setnull=True),
    audience=etl.xstr(r[locs["audience"]-1], setnull=True),
    train_title=etl.xstr(r[locs["train_title"]-1], setnull=True),
    demo_inc=etl.xstr(r[locs["demo_inc"]-1], setnull=True),
    iec_dist=etl.xstr(r[locs["iec_dist"]-1], setnull=True),
    dur_session=etl.xstr(r[locs["dur_session"]-1], setnull=True),
    amt_parti=etl.xstr(r[locs["amt_parti"]-1], setnull=True),
    total_cost=etl.xstr(r[locs["total_cost"]-1], setnull=True),
    total_parti=etl.xstr(r[locs["total_parti"]-1], setnull=True),
    males=etl.xstr(r[locs["males"]-1], setnull=True),
    females=etl.xstr(r[locs["females"]-1], setnull=True),
    third_gen=etl.xstr(r[locs["third_gen"]-1], setnull=True),
    elderly=etl.xstr(r[locs["elderly"]-1], setnull=True),
    children=etl.xstr(r[locs["children"]-1], setnull=True),
    person_dis=etl.xstr(r[locs["person_dis"]-1], setnull=True),
    fem_hh=etl.xstr(r[locs["fem_hh"]-1], setnull=True),
    vuln_hh=etl.xstr(r[locs["vuln_hh"]-1], setnull=True),
    act_status=etl.xstr(r[locs["act_status"]-1], setnull=True),
    start_dt=etl.xstr(r[locs["start_dt"]-1], setnull=True),
    comp_dt=etl.xstr(r[locs["comp_dt"]-1], setnull=True),
    comments=etl.xstr(r[locs["comments"]-1], setnull=True))
    # pk=gen_pk(r, locs))


def gen_pk(r, locs):
    return etl.xstr(r[locs["imp_agency"] - 1].value) + etl.xstr(r[locs["local_partner"] - 1].value) + etl.xstr(
        r[locs["district"] - 1].value) + etl.xstr(r[locs["vdc"] - 1].value) + etl.xstr(
        r[locs["ward"] - 1].value) + etl.xstr(r[locs["act_type"] - 1].value) + etl.xstr(
        r[locs["act_desc"] - 1].value) + etl.xstr(r[locs["quantity"] - 1].value) + etl.xstr(
        r[locs["total_hh"] - 1].value)


def get_locs(ws):
    """find column headers in advance so we don't have to call each time"""
    ret = {}
    ret["priority"] = column_index_from_string(etl.find_in_header(ws, "Priority"))
    ret["access_method"] = column_index_from_string(etl.find_in_header(ws, "Hard to Reach Access Methods"))
    ret["hub"] = column_index_from_string(etl.find_in_header(ws, "Shelter Cluster Hub"))
    ret["as_of"] = column_index_from_string(etl.find_in_header(ws, "Last Update"))
    ret["dist_code"] = column_index_from_string(etl.find_in_header(ws, "District HLCIT Code"))
    ret["vdc_code"] = column_index_from_string(etl.find_in_header(ws, "VDC / Municipality HLCIT Code"))
    ret["uid"] = column_index_from_string(etl.find_in_header(ws, "UID"))

    ret["imp_agency"] = column_index_from_string(etl.find_in_header(ws, "Implementing agency"))
    ret["source_agency"] = column_index_from_string(etl.find_in_header(ws, "Sourcing Agency"))
    ret["local_partner"] = column_index_from_string(etl.find_in_header(ws, "Local partner agency"))
    ret["contact_name"] = column_index_from_string(etl.find_in_header(ws, "Contact Name"))
    ret["contact_email"] = column_index_from_string(etl.find_in_header(ws, "Contact Email"))
    ret["contact_phone"] = column_index_from_string(etl.find_in_header(ws, "Contact Phone Number"))

    ret["district"] = column_index_from_string(etl.find_in_header(ws, "District"))
    ret["vdc"] = column_index_from_string(etl.find_in_header(ws, "VDC / Municipalities"))
    ret["ward"] = column_index_from_string(etl.find_in_header(ws, "Municipal Ward"))

    ret["train_sub"] = column_index_from_string(etl.find_in_header(ws, "Training Subject"))
    ret["audience"] = column_index_from_string(etl.find_in_header(ws, "Audience"))
    ret["train_title"] = column_index_from_string(etl.find_in_header(ws, "Training Title"))
    ret["demo_inc"] = column_index_from_string(etl.find_in_header(ws, "Demonstration Construction Included?"))
    ret["iec_dist"] = column_index_from_string(etl.find_in_header(ws, "IEC Materials Distributed"))
    ret["dur_session"] = column_index_from_string(etl.find_in_header(ws, "Duration of each session (hours)"))
    ret["amt_parti"] = column_index_from_string(etl.find_in_header(ws, "Amount Paid to Participants (NPR per participant)"))
    ret["total_cost"] = column_index_from_string(etl.find_in_header(ws, "Total Cost Per Training"))
    ret["total_parti"] = column_index_from_string(etl.find_in_header(ws, "Total Participants (Individuals)"))
    ret["males"] = column_index_from_string(etl.find_in_header(ws, "Males"))
    ret["females"] = column_index_from_string(etl.find_in_header(ws, "Females"))
    ret["third_gen"] = column_index_from_string(etl.find_in_header(ws, "Third Gender"))
    ret["elderly"] = column_index_from_string(etl.find_in_header(ws, "Elderly (60+)"))
    ret["children"] = column_index_from_string(etl.find_in_header(ws, "Children (under 18)"))
    ret["person_dis"] = column_index_from_string(etl.find_in_header(ws, "Persons with Disabilities"))
    ret["vuln_hh"] = column_index_from_string(etl.find_in_header(ws, "Vulnerable Caste or Ethnicity"))
    ret["fem_hh"] = column_index_from_string(etl.find_in_header(ws, "Female Headed Households (if applicable)"))

    ret["act_status"] = column_index_from_string(etl.find_in_header(ws, "Activity Status"))
    ret["start_dt"] = column_index_from_string(etl.find_in_header(ws, "Start date"))
    ret["comp_dt"] = column_index_from_string(etl.find_in_header(ws, "Completion Date"))

    ret["comments"] = column_index_from_string(etl.find_in_header(ws, "Additional Comments"))
    return ret

if __name__ == '__main__':
    if Base.metadata.tables.has_key('trainings'):
        Base.metadata.tables['trainings'].drop(engine, checkfirst=True)
    Base.metadata.create_all(engine)
    insert_data()
    print 'done'

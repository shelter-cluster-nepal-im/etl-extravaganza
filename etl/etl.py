"""Module for extracting data from dropbox and aggregating"""
#TODO: better way for specifyign which folder to pull from (latest?)
##how to handle names?
##pull from rules based text file
##log put on dbox, make better
##test individual cleaning
##mvoe current logs to an 'old' file 
##put in run params: test, exclude, folder location?
##change to pull down all WSs at same time as opposed to iterating  
##get rid of spcifycing column for uid, should just be one after header
##logs output to local or dbox
##do quick reading method at first for faster run time
##fuzzy match col
##single method to import all file(s) from a path
from collections import Counter

import datetime

import dropbox
import clean
import os
import cStringIO
import re
from openpyxl import load_workbook
from openpyxl.cell import column_index_from_string
from openpyxl import Workbook
import openpyxl.writer.excel as wrtex
import time
import click
from os import listdir
from os.path import isfile, join
from dateutil.parser import parse
from openpyxl.utils import get_column_letter

#dropbox setup
db_access = os.environ['db_access']
client = dropbox.client.DropboxClient(db_access)

@click.command()
@click.option('--act', help='what action will we perform', type = click.Choice(['cons','clean']))
@click.option('--src', help='local files or on dropbox?', type = click.Choice(['db','local']))
@click.option('--path', help='file path (pull all xls or xlsx files in it')
@click.option('--db', help='db file if consolidating')
@click.option('--test', help='are we testing?', is_flag = True)

def iterate_reports(act, src, path, db, test):
    """cycle through all reports contained in dbox directory"""

    file_list = get_file_list(path, src)

    file_list = clean_exclude(act, file_list)

    if test == True:
        file_list = [file_list[0]]


    for v in file_list:
        print v

    #pull down all workbooks
    wbs = []
    for f in file_list:
        #pull down workbook from specified directory
        print "Pulling: " + f
        wb_current = pull_wb(f, src)

        #check to see if properly formatted
        if wb_format(wb_current):
            print 'Appending: ' + f
            wbs.append((wb_current,f))

        else:
            #put in malformatted folder
            print 'Malformatted ' + f
            send_path = path + '/old_format_or_incorrect/' + f.rsplit('/', 1)[1]
            send_wb(send_path, wb_current, src)

    #clean or consolidate
    if act == 'clean':
        #clean workboooks
        for wb in wbs:
            print "Cleaning: " + wb[1]
            clean_file(wb[0], wb[1], src)

    elif act == 'cons':
        #consolidate
        to_send = consolidate(pull_wb(db, src).get_sheet_by_name('Database'), wbs, 'V')
        send_wb(path + 'consolidated.xlsx', to_send, src)

def clean_exclude(act, file_list):
    if act =='clean':
        new_list = []
        for v in file_list:
            if 'C-' in v or 'C -' in v:
                new_list.append(v)
            else:
                print 'Excluding: ' + v
        return new_list

def consolidate(baseline, wsl):
    """consolidate baseline data and worksheets and remove old data"""

    ialoc = find_in_header(baseline,'Implementing Agency')
    base_count = Counter(get_values(baseline.columns[column_index_from_string(ialoc)-1]))

    cons_wb = Workbook()
    cons = cons_wb.active
    cons.title = 'Consolidated'
    cons.append(get_values(baseline.rows[0]))

    to_add = []
    ag_skip = []

    #iterate through each sheet and find entries to be added
    for ws in wsl:
        cd = ws.get_sheet_by_name('Distributions')
        ag_name = cd[str(ialoc + '2')].value
        #check if headers match
        if get_values(cd.rows[0]) != get_values(baseline.rows[0]):
            print '***ERROR: Non-matching header for: ' + xstr(cd[str(ialoc + '2')].value)
        else:
            #check to see if agency is in list and if it is < 80 pct
            if base_count.has_key(ag_name):
                if len(cd.rows) < base_count[ag_name]*.8:
                    print '***WARNING: ' + ag_name + ' is less than 80 pct'
                else:
                    print 'inserting ' + str(len(cd.rows)-1) + ' new values for and removing old for: ' + ag_name
                    ag_skip.append(xstr(ag_name))
                    for r in cd.rows[1:]:
                        to_add.append(get_values(r))
            else:
                print 'inserting ' + str(len(cd.rows)-1) + ' new values for new agency: ' + ag_name
                for r in cd.rows[1:]:
                    to_add.append(get_values(r))

    #create master file
    #this could be better with grouping
    cs = ''
    for v in baseline.rows[1:]:
        if xstr(v[column_index_from_string(ialoc)-1].value) not in ag_skip:
            cons.append(v)
        else:
            if cs != v[column_index_from_string(ialoc)-1].value:
                print 'skipping ' + str(base_count[v[column_index_from_string(ialoc)-1].value]) + ' rows for ' + xstr(v[column_index_from_string(ialoc)-1].value)
                cs = xstr(v[column_index_from_string(ialoc)-1].value)

    #add in new agency info
    for v in to_add:
        cons.append(v)

    return cons_wb



def none_row(val):
    i = (val+val).find(val, 1, -1)
    return None if i == -1 else val[:i]

def keep_dict(row, existing, ws):
    """given conflicting dict entries, return True if current val we should keep
        ...heirarcy of greater status, comp date then started date"""

    status_loc = column_index_from_string(find_in_header(ws, 'Activity Status'))-1
    comp_loc = column_index_from_string(find_in_header(ws, 'Completion Date\n (Actual or Planned)'))-1
    start_loc = column_index_from_string(find_in_header(ws, 'Start date \n(Actual or Planned)'))-1

    #check status
    status = ['Complete', 'Ongoing', 'Plan']
    r_ind = 0
    e_ind = 0

    c=0
    for v in status:
	if row[status_loc].value is None:
	    row[status_loc].value = 'Planned'
	if existing[status_loc] == 'None':
	    existing[status_loc] = 'Planned'

        
	if v in row[status_loc].value:
            r_ind = c
        if v in existing[status_loc]:
            e_ind = c
        c+=1

    #check index
    to_return = False
    if r_ind > e_ind:
        to_return = True

    #check comp date
    if type(row[comp_loc].value) is not datetime.date and type(row[comp_loc].value) is not datetime.datetime and row[comp_loc].value is not None:
        r_v = parse(row[comp_loc].value)
    else:
        r_v = row[comp_loc].value

    if type(existing[comp_loc]) is not datetime.date and type(existing[comp_loc]) is not datetime.datetime and existing[comp_loc] != 'None':
	e_v = parse(existing[comp_loc])
    else:
        e_v = existing[comp_loc]

    if row[comp_loc].value is not None and existing[comp_loc] != 'None':
        if r_v < e_v:
            to_return = True

    #check start date

    if type(row[start_loc].value) is not datetime.date and type(row[start_loc].value) is not datetime.datetime and row[start_loc].value is not None:
        r_v = parse(row[start_loc].value)
    else:
        r_v = row[start_loc].value

    if type(existing[start_loc]) is not datetime.date and type(existing[start_loc]) is not datetime.datetime and existing[start_loc] != 'None':
        e_v = parse(existing[start_loc])
    else:
        e_v = existing[start_loc]

    if row[start_loc].value is not None and existing[start_loc] != 'None':
	if r_v < e_v:
            to_return = True

    return to_return



def get_uid(row, sheet):
    """return a row's UID based on criteria"""
    vals = ["Implementing agency", "Local partner agency" , "District", 
            "VDC / Municipalities", "Municipal Ward", "Action type", 
            "Action description", "# Items / # Man-hours / NPR",
            "Total Number Households"]
    key = ""

    for v in vals:
        try:
            key += xstr(row[column_index_from_string(find_in_header(sheet, v))-1].value)
        except:
            print 'broken!! ' + str(sheet)

    return key

def get_values(r):
    """returns values of a row or a column"""
    return [xstr(v.value) for v in r]

def send_wb(path, wb, src):
    print 'Sending: ' + path
    if src == 'db':
        client.put_file(path, wrtex.save_virtual_workbook(wb))

    elif src == 'local':
        print 'path is ' + path
        print 'splt ' + path.rsplit('/', 1)[0]
        if not os.path.exists(path.rsplit('/', 1)[0]):
            print '**Doesnt exist'
            os.makedirs(path.rsplit('/', 1)[0])
        wb.save(path)



def wb_format(wb):
    """check to see if a report is correct and in the new report format"""
    must_contain = ['Distributions', 'Training', 'Reference']

    match_count = 0
    for s in wb.worksheets:
        if s.title in must_contain:
            match_count+=1

    if match_count < 3:
        return False
    else:
        return True

def clean_file(wb, path, src):
    """cycle through a report and apply cleaning algorithms"""
    
    #get our two sheets
    db = wb.get_sheet_by_name('Distributions')
    ref = wb.get_sheet_by_name('Reference')

    #setup log
    rname =  path.rsplit('/', 1)[1]
    report_line = '******Report for ' + rname + ' ******'
    report_a_log(report_line, rname)


    #####do edit stuff
    #algos return db, ref, message

    #algo1
    db, ref, message = clean.algo1(db,ref) 
    report_a_log(message, rname)

    #algo2
    db, ref, message = clean.algo2(db,ref)
    report_a_log(message, rname)

    #algo3
#    db, ref, message = clean.algo3(db,ref)
#    report_a_log(message, rname)

    #algo4
    db, ref, message = clean.algo4(db,ref)
    report_a_log(message, rname)

    #algo5
    db, ref, message = clean.algo5(db,ref)
    report_a_log(message, rname)

    #algo6
    db, ref, message = clean.algo6(db,ref)
    report_a_log(message, rname)

    #algo7
    db, ref, message = clean.algo7(db,ref)
    report_a_log(message, rname)

    #algo8
    db, ref, message = clean.algo8(db,ref)
    report_a_log(message, rname)

    #algo9
    db, ref, message = clean.algo9(db,ref)
    report_a_log(message, rname)

    #algo10
    db, ref, message = clean.algo10(db,ref)
    report_a_log(message, rname)

    #algo11
    db, ref, message = clean.algo11(db,ref)
    report_a_log(message, rname)

    #algo12
    db, ref, message = clean.algo12(db,ref)
    report_a_log(message, rname)

    #algo13
    db, ref, message = clean.algo13(db,ref)
    report_a_log(message, rname)

    #algo14
    db, ref, message = clean.algo14(db,ref)
    report_a_log(message, rname)

    #algo15
    db, ref, message = clean.algo15(db,ref)
    report_a_log(message, rname)

    #algo16
    db, ref, message = clean.algo16(db,ref)
    report_a_log(message, rname)

    #algo17
    db, ref, message = clean.algo17(db,ref)
    report_a_log(message, rname)

    #algo18
    db, ref, message = clean.algo18(db,ref)
    report_a_log(message, rname)

    #algo19
    db, ref, message = clean.algo19(db,ref)
    report_a_log(message, rname)


    #dummy empty log to send to finalize logging
    report_a_log(' ','text')

    #upload with name of file at end
    #we need to upload the new version!!!!!!!!
    send_wb(path.rsplit('/', 1)[0] + '/edited/' + path.rsplit('/', 1)[1], wb, src)
    print 'uploaded! ' + path.rsplit('/', 1)[0] + '/edited/' + path.rsplit('/', 1)[1]

report_recvd = False
current_path = ''
current_log = []

def report_a_log(log_value, path):
    """write out contents for a given log - creates new entry if a new path is given"""
    #todo: this is gross
    global report_recvd
    global current_path
    global current_log


    #if module is starting and we haven't logged anything
    if not report_recvd:
        current_path = path
        report_recvd = True
    

    #if we are recieving a new path
    elif current_path != path:
        current_path = path
        
        #write out
        with open('/Users/ewanog/code/nepal-earthquake/shelter/etl-extravaganza/etl/logs/'+
            time.strftime("%m-%d-%y_%H:%M_%S") +'.txt', 'w') as f:
            for log in current_log:
                f.write(str(log)+'\n')
        f.close()

        #move on to next log
        current_log.append('')
        current_log.append('')

    current_log.append(log_value)
    current_log.append('')



def find_in_header(sheet, find_val):
    """find the coordinate of a value in header (assumes header is in row 1)"""
    for row in sheet.iter_rows('A1:' + find_last_value(sheet,'A','r')):
        for cell in row:
            if cell.value.replace(' ','').replace('\n','').lower() == find_val.replace(' ','').replace('\n','').lower():
                return cell.column

    #if we haven't returned anything yet, try fuzzy match
    print 'No header found for: ' + find_val
    return None

def colvals_notincol(sheet_val,col_val,sheet_ref,col_ref):
    """return values from a column that are NOT in a reference column"""
    not_in = []
    to_search = []

    #create an array from sheet_ref with values to be searched (as opposed to nested loops)
    #iter_rows syntax: sheet.iter_rows('A1:A2')
    for row in sheet_ref.iter_rows(col_ref + "2:" + 
        find_last_value(sheet_ref, col_ref, 'c')):

        for cell in row:               
                try:
                    to_search.append(xstr(cell.value))
                except:
                    to_search.append(str(cell.value))

    #now search through vals and see if they're present
    for row in sheet_val.iter_rows(col_val + "2:" + 
        find_last_value(sheet_val, col_val, 'c')):

        for cell in row:
            if xstr(cell.value) not in to_search:
                try:
                    not_in.append(xstr(cell.value))
                except:
                    not_in.append(str(cell.value))

    return not_in
             


def find_last_value(sheet, start_location, r_or_c):
    """find position of last value in a given row or column - if row, we assume header"""
    #extract form r_or_c if we should be iterating a row or column
     #this has been deprecated in favor of openpyxl features - all methods should change their calls

    if r_or_c == 'c':
        return start_location + str(sheet.max_row)
    elif r_or_c == 'r':
        return get_column_letter(sheet.max_column) + '1'
    else:
        raise Exception("r_or_c must be r or c!")


def pull_wb(location, src):
    """return an excel file from either local or source"""

    return wb_strip(location, src)

def wb_strip(location, src):
    if src == 'db':
        w = load_workbook(pull_from_db(location), read_only = True, data_only = True)

    else:
        w = load_workbook(location, read_only = True, data_only = True)

    new_wb = Workbook()
    new_wb.remove_sheet(new_wb.worksheets[0])
    for v in w.worksheets:
        cur_w = new_wb.create_sheet(1, v.title)
        for r in v.rows:
            for v in r:
                if v.value is not None:
                    cur_w[v.coordinate] = v.value

    print "Pulled: " + location
    print "With tabs: " + str(new_wb.get_sheet_names())

    return new_wb

def pull_from_db(location):
    """pull a file from dropbox"""
    to_ret = cStringIO.StringIO()

    with client.get_file(location) as f:
        to_ret.write(f.read())
    f.close()

    return to_ret

def get_file_list(path, src):
    """return file list from local or db"""
    if src == 'db':
        meta = client.metadata(path, list=True)
        return [str(f['path']) for f in meta['contents'] if re.search('xls|xlsx$',str(f))]

    elif src == 'local':
        return [str(path +'/' + f) for f in listdir(path) if isfile(join(path,f)) and re.search('xls|xlsx$',str(f))]

def fuzzy_match_col(col, vals):
    False

def xstr(conv):
    """return a properly encoded string"""
    try:
        return str(conv.encode('utf8'))
    except:
        return str(conv)

def test():
    return load_workbook('/Users/ewanog/code/nepal-earthquake/shelter/etl/clean_test.xlsx', data_only=True)

if __name__ == '__main__':
    iterate_reports()

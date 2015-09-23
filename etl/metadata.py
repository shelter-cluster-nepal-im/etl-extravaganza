"""methods for retreiving metadata"""

import etl
from openpyxl.cell import column_index_from_string

class Meta:

    def priority(self, db):
        """is it a priority district"""
        dloc = column_index_from_string(etl.find_in_header(db, 'District'))-1
        rloc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'Priority Districts'))-1

        dvals = etl.get_values(db.columns[dloc][1:])
        rvals = etl.get_values(self.s_dict['ref'].columns[rloc][1:])
        ret = []

        for v in dvals:
            if v in rvals and v != '':
                ret.append('TRUE')
            else:
                ret.append('FALSE')

        return ret

    def reach(self, db):
        """how is the vdc accessible"""
        #TODO: use index() method instead of dict
        dist_loc = column_index_from_string(etl.find_in_header(db, 'District'))-1
        vdc_loc = column_index_from_string(etl.find_in_header(db, 'VDC / Municipalities'))-1
        acc_look = column_index_from_string(etl.find_in_header(self.s_dict['acc'], 'DistrictVDC Concatenation'))-1
        acc_acc = column_index_from_string(etl.find_in_header(self.s_dict['acc'], 'NeKSAP ACCESS'))-1

        dist_vals = etl.get_values(db.columns[dist_loc][1:])
        vdc_vals = etl.get_values(db.columns[vdc_loc][1:])
        acc_look_vals = etl.get_values(self.s_dict['acc'].columns[acc_look][1:])
        acc_acc_vals =  etl.get_values(self.s_dict['acc'].columns[acc_acc][1:])

        #make dict for access, concatenate dist and vdc
        acc_dict = dict(zip(acc_look_vals, acc_acc_vals))
        d_v_conc = [dist_vals[i] + vdc_vals[i] for i in xrange(len(dist_vals))]

        ret = []
        for v in d_v_conc:
            if v in acc_dict and v != '':
                ret.append(acc_dict[v])
            else:
                ret.append('')

        return ret

    def hub(self, db):
        "what a hub a dist is in"
        dloc = column_index_from_string(etl.find_in_header(db, 'District'))-1
        pri_rloc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'Priority Districts'))-1
        hub_rloc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'Shelter Cluster Hubs'))-1

        dvals = etl.get_values(db.columns[dloc][1:])
        pri_rloc_vals = etl.get_values(self.s_dict['ref'].columns[pri_rloc][1:])
        hub_rloc_vals = etl.get_values(self.s_dict['ref'].columns[hub_rloc][1:])
        ret = []

        for v in dvals:
            if v in pri_rloc_vals and v != '':
                ret.append(hub_rloc_vals[pri_rloc_vals.index(v)])
            else:
                ret.append('')

        return ret

    def update(self, db):
        "last updated"
        dloc = column_index_from_string(etl.find_in_header(db, 'Last Update'))-1
        dvals = etl.get_values(db.columns[dloc][1:])
        to_ret = []

        for v in dvals:
            to_ret.append(v)

        return to_ret


    def dist_hlcit(self, db):
        "dist code"
        dloc = column_index_from_string(etl.find_in_header(db, 'District'))-1
        d_rloc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'Admin1_District'))-1
        code_rloc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'Admin1_P-Code'))-1

        dvals = etl.get_values(db.columns[dloc][1:])
        d_rloc_vals = etl.get_values(self.s_dict['ref'].columns[d_rloc][1:])
        code_rloc_vals = etl.get_values(self.s_dict['ref'].columns[code_rloc][1:])
        ret = []

        for v in dvals:
            if v in d_rloc_vals and v != '':
                ret.append(code_rloc_vals[d_rloc_vals.index(v)])
            else:
                ret.append('')

        return ret

    def vdc_hlcit(self, db):
        """how is the vdc accessible"""
        #TODO: use index() method instead of dict
        dist_loc = column_index_from_string(etl.find_in_header(db, 'District'))-1
        vdc_loc = column_index_from_string(etl.find_in_header(db, 'VDC / Municipalities'))-1
        acc_look = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'Admin1 + Admin2 Concatenation'))-1
        acc_acc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'Admin2_HLCIT_CODE'))-1

        dist_vals = etl.get_values(db.columns[dist_loc][1:])
        vdc_vals = etl.get_values(db.columns[vdc_loc][1:])
        acc_look_vals = etl.get_values(self.s_dict['ref'].columns[acc_look][1:])
        acc_acc_vals =  etl.get_values(self.s_dict['ref'].columns[acc_acc][1:])

        #make dict for access, concatenate dist and vdc
        acc_dict = dict(zip(acc_look_vals, acc_acc_vals))
        d_v_conc = [dist_vals[i] + vdc_vals[i] for i in xrange(len(dist_vals))]

        ret = []
        for v in d_v_conc:
            if v in acc_dict and v != '':
                ret.append(acc_dict[v])
            else:
                ret.append('')

        return ret

    def act_cat(self, db):
        "UNOCHA cat"
        dloc = column_index_from_string(etl.find_in_header(db, 'Action description'))-1
        sc_rloc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'SC Categories'))-1
        un_rloc = column_index_from_string(etl.find_in_header(self.s_dict['ref'], 'UN Categories'))-1

        dvals = etl.get_values(db.columns[dloc][1:])
        sc_rloc_vals = etl.get_values(self.s_dict['ref'].columns[sc_rloc][1:])
        un_rloc_vals = etl.get_values(self.s_dict['ref'].columns[un_rloc][1:])
        ret = []

        for v in dvals:
            if v in sc_rloc_vals and v != '':
                ret.append(un_rloc_vals[sc_rloc_vals.index(v)])
            else:
                ret.append('')

        return ret

    def uid(self, db):
        "UID"
        ok_key = False
        if db.title == 'Distributions':
            vals = ["Implementing agency", "Local partner agency" , "District",
                    "VDC / Municipalities", "Municipal Ward", "Action type",
                    "Action description", "# Items / # Man-hours / NPR",
                "Total Number Households"]
            ok_key = True

        elif db.title == 'Trainings':
            vals = ["Implementing agency","Local partner agency","District","VDC / Municipalities","Municipal Ward",
                    "Training Subject","Audience","IEC Materials Distributed","Males"]
            ok_key = True

        to_ret = []
        if ok_key:


            for r in db.rows[1:]:
                key = ""
                for v in vals:
                    try:
                        key += etl.xstr(r[column_index_from_string(etl.find_in_header(db, v))-1].value)
                    except:
                        print 'Malformmated UID for: ' + etl.xstr(r[column_index_from_string(etl.find_in_header \
                                    (db, 'Implementing agency'))-1].value) + ' for WS: ' + db.title
                to_ret.append(key)

            return to_ret

        else:
            return to_ret
            print 'ERROR: no suitable WB found for UID'


    def get(self, col, db):
        return self.cols[col](db)

    def __init__(self, ref_sht, acc_sht, codes_sht):
        self.s_dict = {'ref' : ref_sht, 'acc' : acc_sht, 'codes' : codes_sht}

        self.cols = {
                       "Priority" : self.priority,
                       "Hard to Reach Access Methods" : self.reach,
                       "Shelter Cluster Hub" : self.hub,
                       "Last Update" : self.update,
                       "District HLCIT Code" : self.dist_hlcit,
                       "VDC / Municipality HLCIT Code" : self.vdc_hlcit,
                       "UNOCHA Activity Categories" : self.act_cat,
                       "UID" : self.uid
                    }

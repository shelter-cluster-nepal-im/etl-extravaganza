"""excel sheet object - all teh dataz"""
import etl

class Sheet:

    def get_col_nms(self, col_nms):
        """return a dict containg raw header names and associated shortned name. Shortened deafults to header names"""
        if col_nms is not None:
            return dict(zip(self.col_nms, self.values[0]))
        else:
            return dict(zip(self.values[0] , self.values[0]))

    def __init__(self, **kargs):
        self.values = etl.get_all_values_from_ws(kargs['ws'])
        self.name = kargs['name']

        cn = None
        if kargs['col_nms'] is not None:
            cn = kargs['col_nms']
        self.col_nms = self.get_col_nms(cn)


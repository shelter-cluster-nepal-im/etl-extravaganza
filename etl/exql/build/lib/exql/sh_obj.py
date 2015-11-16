"""excel sheet object - all teh dataz"""
import etl

class sh_obj:

    def get_col_nms(self, col_nms):
        if col_nms is not None:
            return tuple(col_nms)

        else:
            return tuple(self.values[0])

    def __init__(self, values, path, col_nms):
        self.values = etl.get_all_values_from_ws(values)
        self.name = path.split('/')[-1]
        self.col_nms = get_col_nms(col_nms)


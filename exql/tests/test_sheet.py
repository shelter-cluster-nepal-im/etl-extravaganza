import unittest
from exql.Sheet import Sheet
import etl
from openpyxl import load_workbook
from openpyxl import Workbook

class TestUpload(unittest.TestCase):

    def test_get_col_nms_not_provided(self):
        ws = Workbook().get_active_sheet()
        ws.append(('col1','col2'))
        s = Sheet(ws = ws, name = 'test')
        self.assertEqual(s.col_nms, ('col1','col2'))

if __name__ == '__main__':
    unittest.main()

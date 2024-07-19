import unittest
from src.database_connection import DatabaseConnectionObject

class dbc_tester(unittest.TestCase):
    def test_dbc_param(self):
        """Testing parameters' type check of a dataBaseConnectionObject."""
        failing_lst = [-1, 1, 1.32, (1, 2), {}, []]
        passing_lst = ["https://ows.rasdaman.org/rasdaman/ows"]
        failing_cvg_lst = [1, 2.3, {}, []]
        passing_cvg_lst = ["https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities"]

        for test_case in failing_lst:
            try:
                DatabaseConnectionObject(test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")
        
        for test_case in passing_lst:
            try:
                DatabaseConnectionObject(test_case)
            except ValueError:
                self.fail(f"test case: {test_case} failed.")
        
        for test_case_1 in failing_lst:
            for test_case_2 in failing_cvg_lst:
                try:
                    DatabaseConnectionObject(test_case_1, test_case_2)
                except ValueError:
                    pass
                else:
                    self.fail(f"Test cases: {test_case_1}, {test_case_2} failed.")
                    
        for test_case_1 in passing_lst:
            for test_case_2 in failing_cvg_lst:
                try:
                    DatabaseConnectionObject(test_case_1, test_case_2)
                except ValueError:
                    pass
                else:
                    self.fail(f"Test cases: {test_case_1}, {test_case_2} failed.")

        for test_case_1 in passing_lst:
            for test_case_2 in passing_cvg_lst:
                try:
                    DatabaseConnectionObject(test_case_1, test_case_2)
                except ValueError:
                    self.fail(f"Test cases: {test_case_1}, {test_case_2} failed.")

    def test_dbc_pre_processing_behaivour(self):
        """Testing dataBaseConnectionObject's pre_processing behaivour."""
        failing_cvg_lst = ["", "https://nearly_any_other_website.com", "differentFormatting", "shouldAlsoLead", "toTheSameThing"]
        passing_cvg_lst = ["https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities"]
        
        for test_case in failing_cvg_lst:
            dbc = DatabaseConnectionObject("doesn_t_matter", test_case)
            
            if dbc.pre_processed_coverage_support == True:
                self.fail(f"test case: {test_case} failed.")
            else:
                if dbc.pre_processed_coverage_dict != None:
                    self.fail(f"test case: {test_case} failed.")

        for test_case in passing_cvg_lst:
            dbc = DatabaseConnectionObject("doesn_t_matter", test_case)
            
            if dbc.pre_processed_coverage_support == False:
                self.fail(f"test case: {test_case} failed.")
            else:
                if dbc.pre_processed_coverage_dict == {}:
                    self.fail(f"test case: {test_case} failed.")



if __name__ == '__main__':
    unittest.main()

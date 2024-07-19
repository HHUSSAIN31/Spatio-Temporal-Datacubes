import unittest
from src.get_coverage import formatText, isBlank, getAvailableRequests, processedDataIntoList


class get_coverage_functions_tester(unittest.TestCase):
    def test_formatText(self):
        """Testing the behaivour of formatText function."""
        failing_lst = [-1, 1, 1.32, (1, 2), {}, []]
        passing_unchanged_lst = ["", "nothing", "d0s3n't_matter"]
        passing_changed_lst = [["", ""], ["{some}some", "some"], ["some{some}", ""], ["{nada", "{nada"]]

        for test_case in failing_lst:
            try:
                formatText(test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in passing_unchanged_lst:
            try:
                formatText(test_case)
            except ValueError:
                self.fail(f"test case: {test_case} failed.")

        for pair in passing_changed_lst:
            test_case_1 = pair[0]
            expected_result = pair[1]
            test = formatText(test_case_1)
            if test != expected_result:
                self.fail(f"test case: {test_case_1}, {expected_result} failed.")

    def test_isBlank(self):
        """Testing the behaivour of isBlank function."""
        failing_lst = [-1, 1, 1.32, (1, 2), {}, []]
        passing_false_lst = ["}.l{something", " 1", "1 ", "\n\n1\n\n", "\r1", "\t.\t"]
        passing_true_lst = ["\t", "\n", "\r", "\t\n\r", "\n\r", "\r\t", "\t\n"]

        for test_case in failing_lst:
            try:
                isBlank(test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in passing_false_lst:
            if isBlank(test_case) != False:
                self.fail(f"test case: {test_case} failed.")
        
        for test_case in passing_true_lst:
            if isBlank(test_case) != True:
                self.fail(f"test case: {test_case} failed.")

    def test_getAvailableRequests(self):
        """Testing the behaivour of getAvailableRequests function."""
        failing_lst_param_1 = [-1, 1, 1.32, (1, 2), {}, []]
        failing_lst_param_2 = [-1, "", 1.32, (1, 2), {}, []]
        passing_lst_param_1 = ["", "some_server.com"]
        passing_lst_param_2 = [True, False]
        passing_to_be_checked_param_1 = ["https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities"]

        for test_case in failing_lst_param_1:
            try:
                getAvailableRequests(test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_param_2:
            try:
                getAvailableRequests("", test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")
        
        for test_case in passing_lst_param_1:
            try:
                val = getAvailableRequests(test_case)
                if val != []:
                    self.fail(f"test case: {test_case} failed.")    
            except ValueError:
                self.fail(f"test case: {test_case} failed.")

        for test_case in passing_to_be_checked_param_1:
            try:
                val = getAvailableRequests(test_case)
                if val == []:
                    self.fail(f"test case: {test_case} failed. Might be the internet connection")    
            except ValueError:
                self.fail(f"test case: {test_case} failed.")

        for test_case_1 in passing_lst_param_1:
            for test_case_2 in passing_lst_param_2:
                try:
                    val = getAvailableRequests(test_case_1, test_case_2)
                    if val != []:
                        self.fail(f"test case: {test_case} failed. Response Formatting might have changed")
                except ValueError:
                    self.fail(f"test case: {test_case} failed.")

    def test_processDataIntoList(self):
        """Testing the behaivour of processDataIntoList function."""
        failing_lst_param_1 = [-1, 1, 1.32, (1, 2), {}, []]
        failing_lst_param_2 = [-1, "", 1.32, (1, 2), {}, []]
        passing_lst_param_1 = ["", "some_server.com"]
        passing_lst_param_2 = [True, False]
        passing_to_be_checked_param_1 = ["https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities"]

        for test_case in failing_lst_param_1:
            try:
                processedDataIntoList(test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")

        for test_case in failing_lst_param_2:
            try:
                processedDataIntoList("", test_case)
            except ValueError:
                pass
            else:
                self.fail(f"test case: {test_case} failed.")
        
        for test_case in passing_lst_param_1:
            try:
                val = processedDataIntoList(test_case)
                if val[0] != [] or val[1] != 0:
                    self.fail(f"test case: {test_case} failed.")    
            except ValueError:
                self.fail(f"test case: {test_case} failed.")

        for test_case in passing_to_be_checked_param_1:
            try:
                val = processedDataIntoList(test_case)
                if val[0] == []:
                    self.fail(f"test case: {test_case} failed. Might be the internet connection")    
            except ValueError:
                self.fail(f"test case: {test_case} failed.")

        for test_case_1 in passing_lst_param_1:
            for test_case_2 in passing_lst_param_2:
                try:
                    val = processedDataIntoList(test_case_1, test_case_2)
                    if val[0] != []:
                        self.fail(f"test case: {test_case} failed. Response Formatting might have changed")
                except ValueError:
                    self.fail(f"test case: {test_case} failed.")




if __name__ == '__main__':
    unittest.main()

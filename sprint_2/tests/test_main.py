'''test.py File:
Purpose: A test.py file contains automated tests to verify the correctness and reliability of  code.
Importance:
Validates that  code behaves as expected under various conditions and inputs.
Helps catch bugs, regressions, and edge cases early in the development process.
Facilitates code maintenance and refactoring by ensuring that existing functionality remains intact after modifications.
Supports continuous integration and collaboration by providing a standardized way to run tests automatically.
Content:
Includes test cases written using a testing framework like unittest, pytest, or nose.
Covers different aspects of your codebase, including individual functions, classes, and modules.
Tests both typical and edge cases to ensure comprehensive coverage.
Provides assertions to validate expected outcomes against actual results.'''
import unittest
from main import *

class TestMain(unittest.TestCase):
    def setUp(self):
        self.url = 'https://ows.rasdaman.org/rasdaman/ows'
        self.dbc = DatabaseConnection(self.url)
        self.datacube = Datacube(self.dbc)

    def test_subset_temperature(self):
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        response, wcps_query = self.datacube.subset_temperature(region, time_range)
        self.assertTrue(response)
        self.assertTrue(wcps_query)

    # Add more test cases for other methods as needed

if __name__ == '__main__':
    unittest.main()

import unittest
from dco import Datacube
from dbc import DatabaseConnection

class TestDatacube(unittest.TestCase):
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

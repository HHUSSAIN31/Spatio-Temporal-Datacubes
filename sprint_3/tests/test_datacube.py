import unittest
from src.datacube import DatacubeObject
from src.database_connection import DatabaseConnectionObject

class TestDco(unittest.TestCase):
    def setUp(self):
        # Initialize any objects needed for testing
        self.coverage1 = "AvgLandTemp"
        self.dbc = DatabaseConnectionObject("https://ows.rasdaman.org/rasdaman/ows", "https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities")
        self.datacube1 = DatacubeObject(self.dbc, self.coverage1)
        self.coverage2 = "mean_summer_airtemp"
        self.datacube2 = DatacubeObject(self.dbc, self.coverage2)
        
        self.new_datacube = DatacubeObject(self.dbc)
        self.coverage_var = "AvgLandTemp"
        self.encoding = "jpeg"

        self.datacube = DatacubeObject(self.dbc, "NIR")
        
    def test_init_(self):
        with self.assertRaises(TypeError):
            self.temp = DatacubeObject([], "AvgLandTemp")
        with self.assertRaises(TypeError):
            self.temp = DatacubeObject(self.dbc, 3)

    def test_create_datacube(self):
        try:
            self.datacube1.create_datacube()
        except Exception as e:
            print(e)
    
    def test_check_lat(self):
        try:
            self.datacube1.check_lat(90)
            self.datacube1.check_lat(-60)
        except ValueError:
            self.fail("Valid latitude ranges raised ValueError")

        with self.assertRaises(ValueError):
            self.datacube1.check_lat(99)

        try:
            self.datacube1.check_lat("str")
            self.datacube1.check_lat([])
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError not raised")

        #When the meta data cannot be checked
        self.dbc.pre_processed_coverage_dict = {}
        with self.assertRaises(Exception):
            self.datacube1.check_lat(70)
    
    def test_check_lon(self):
        try:
            self.datacube1.check_lon(80)
            self.datacube1.check_lon(-60)
        except ValueError:
            self.fail("Valid longitude ranges raised ValueError")

        with self.assertRaises(ValueError):
            self.datacube1.check_lon(190)
        try:
            self.datacube1.check_lat("str")
            self.datacube1.check_lat([])
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError not raised")

        #When the meta data cannot be checked
        self.dbc.pre_processed_coverage_dict = {}
        with self.assertRaises(Exception):
            self.datacube1.check_lat(70)

    def test_check_dates(self):
        try:
            self.datacube1.check_years("2012-07", "2012-08")
            self.datacube1.check_years("2012-07", "2014-07")
            self.datacube1.check_years("2012-07-01", "2012-08-30")
            self.datacube1.check_years("2012-07")
        except ValueError:
            self.fail("Valid date ranges raised ValueError")

        with self.assertRaises(TypeError):
            self.datacube1.check_lat(2012, 2014)

        try:
            self.datacube1.check_years("2012/01", "2012-02")
            self.datacube1.check_years("2012-01", "2012/02")
            self.datacube1.check_years("2012:01")
            self.datacube1.check_years("", "2012-01")
            self.datacube1.check_years("2012-08", "")
            self.datacube1.check_years("", "")
            self.datacube1.check_years("2012-09", "2020-10")
            self.datacube1.check_years("2020-09", "2020-10")
            self.datacube1.check_years("2014-06", "2012-03")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")

        #When the meta data cannot be checked
        self.dbc.pre_processed_coverage_dict = {}
        with self.assertRaises(Exception):
            self.datacube1.check_lat("2014-04")

    def test_subset(self):
        try:
            self.datacube1.subset("Lat", 53)
            self.datacube1.subset("Long", 90)
            self.datacube1.subset("Lat", "55:80")
            self.datacube1.subset("Long", "-90:-100")
        except ValueError:
            self.fail("Valid data raised ValueError")
            
        try:
            self.datacube1.subset([], 10)
            self.datacube1.subset("Lat", [])
            self.datacube1.subset([], [])
        except TypeError:
            pass
        else: 
            self.fail("Expected ValueError was not raised")
               
        try:
            self.datacube1.subset("", 60)
            self.datacube1.subset("Latitude", 60)
            self.datacube1.subset("Lat", -99)
            self.datacube1.subset("Long", 188)
            self.datacube1.subset("Lat", "50:99")
            self.datacube1.subset("Long", "170:188")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")

        #When the meta data cannot be checked
        self.dbc.pre_processed_coverage_dict = {}
        with self.assertRaises(Exception):
            self.datacube1.check_lat(70)

    def test_execute(self):
        try:
            self.datacube1.subset("Lat", 53).subset("Long", 54).timerange("2012-03", "2014-08").add_condition("+", 30).execute()
            self.datacube2.subset("Lat", -30).subset("Long", 140).to_Kelvin().execute()
        except ValueError:
            self.fail("Valid data raised ValueError")
        
    def test_add_condition(self):
        try:
            self.datacube1.add_condition(">=", 20)
            self.datacube1.add_condition("+", 30)
            self.datacube1.add_condition("*", 3)
            self.datacube1.add_condition("*", 3.5)
        except ValueError:
            self.fail("Valid data raised ValueError")

        try:
            self.datacube1.add_condition("=", 30)
            self.datacube1.add_condition("@", 3)
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")
    
        try:
            self.datacube1.add_condition(["=="], 30)
            self.datacube1.add_condition(">=", "3")
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")

    def test_aggregate(self):
        try:
            self.datacube1.aggregate("max", ">=", 20)
            self.datacube1.aggregate("min", "<=", 12)
            self.datacube1.aggregate("max")
        except ValueError:
            self.fail("Valid data raised ValueError")

        try:
            self.datacube1.aggregate("add")
            self.datacube1.aggregate("add", ">=", 3)
            self.datacube1.aggregate("min", "*", 30)
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")
    
        try:
            self.datacube1.add_condition(["=="], 30)
            self.datacube1.add_condition(">=", "3")
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")

    def test_timerange(self):
        try:
            self.datacube1.timerange("2012-12")
            self.datacube1.timerange("2012-06", "2014-03")
        except ValueError:
            self.fail("Valid data raised ValueError")

        with self.assertRaises(TypeError):
            self.datacube1.timerange(2012, 2014)

        try:
            self.datacube1.timerange("2012/01", "2012-02")
            self.datacube1.timerange("2012-01", "2012/02")
            self.datacube1.timerange("2012:01")
            self.datacube1.timerange("", "2012-01")
            self.datacube1.timerange("2012-08", "")
            self.datacube1.timerange("", "")
            self.datacube1.timerange("2012-09", "2020-10")
            self.datacube1.timerange("2020-09", "2020-10")
            self.datacube1.timerange("2014-06", "2012-03")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")

        #When the meta data cannot be checked
        self.dbc.pre_processed_coverage_dict = {}
        with self.assertRaises(Exception):
            self.datacube1.check_lat("2014-04")

    def test_encode(self):
        try:
            self.datacube1.encode("csv")
            self.datacube1.encode("png/image")
        except ValueError:
            self.fail("Valid data raised ValueError")

        with self.assertRaises(TypeError):
            self.datacube1.encode([])
    
    def test_to_Kelvin(self):
        try:
            self.datacube1.to_Kelvin()
        except ValueError:
            self.fail("Valid data raised ValueError")

    def test_color_switching(self):
        dict_correct = {10 : [255, 255, 255], 30 : [0, 0, 0]}
        dict_wrong1 = {10 : [255, 255, 255], 30 : [0, 0]}
        dict_wrong2 = {10 : [255, 255, 255], 30 : [0, 0, "0"]}
        dict_wrong3 = {"10" : [255, 255, 255], 30 : [0, 0]}
        
        try:
            self.datacube1.color_switching(dict_correct)
        except ValueError:
            self.fail("Valid data raised ValueError")
        
        try:
            self.datacube1.color_switching(dict_wrong1)
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")

        try:
            self.datacube1.color_switching(dict_wrong2)
            self.datacube1.color_switching(dict_wrong3)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
    
    def test_polygon(self):
        polygon_coordinate_2d_correct = [(-10.3829, 132.0117), (-35.4314, 140.4102), (-40.3151, 153.7891)]
        polygon_coordinate_3d_correct = [(-10.3829, 132.0117, "2012-01"), (-35.4314, 140.4102, "2012-03"), (-40.3151, 153.7891, "2012-12")]
        polygon_coordinate_2d_incorrect = [(-10.3829, 132.0117), (-35.4314, 140.4102)]
        polygon_coordinate_3d_incorrect = [(-10.3829, 132.0117, "2012-01"), (-35.4314, 140.4102, "2012-03"), (-40.3151, 153.7891)]

        try:
            self.datacube1.polygon(polygon_coordinate_3d_correct)
            self.datacube2.polygon(polygon_coordinate_2d_correct)
        except ValueError:
            self.fail("Valid data raised ValueError")

        try: 
            self.datacube1.polygon(polygon_coordinate_3d_incorrect)
            self.datacube2.polygon(polygon_coordinate_2d_incorrect)
            self.datacube1.polygon(polygon_coordinate_2d_correct)
            self.datacube2.polygon(polygon_coordinate_3d_correct)
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")

        with self.assertRaises(TypeError):
            self.datacube1.polygon(dict)

    def test_getitem_(self):        
        try:
            self.datacube1[0, 10:20, 30]
            self.datacube1[0:10:2, 20:30, :]
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")
    
    def test_extract_variables(self):
        try:
            result = self.new_datacube.extract_variables("$c, $d + $variable")
            expected_result = ["$c", "$d", "$variable"]
            self.assertEqual(result, expected_result)
        except ValueError:
            self.fail("Valid data raised ValueError")
            
        try: 
            self.new_datacube.extract_variables("variable")
            self.new_datacube.extract_variables("c")
            self.new_datacube.extract_variables("@d")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
    
        try:
            self.new_datacube.extract_variables([])
            self.new_datacube.extract_variables(["$c"])
            self.new_datacube.extract_variables(44)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")  
            
    def test_var_existence(self):
        self.new_datacube.d_query_vars = ["$c", "$d", "$variable"]
        try:
            result = self.new_datacube.var_existence("$c, $d + $variable")
            self.assertEqual(result, True)
        except ValueError:
            self.fail("Valid data raised ValueError")
            
        try: 
            self.new_datacube.var_existence("variable")
            self.new_datacube.var_existence("$c")
            self.new_datacube.var_existence("$variable + $d")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
        
        try:
            self.new_datacube.var_existence([])
            self.new_datacube.var_existence(["$c"])
            self.new_datacube.var_existence(44)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
    
    def test_init_var(self):
        try:
            self.new_datacube.init_var("AvgLandTemp", "c")
            self.new_datacube.init_var("AvgTemperatureColor", "d")
            expected_variables = ["$c", "$d"]
            expected_coverages = ["AvgLandTemp", "AvgTemperatureColor"]
            self.assertEqual(expected_variables, self.new_datacube.d_query_vars)
            self.assertEqual(expected_coverages, self.new_datacube.d_coverages)
        except ValueError:
            self.fail("Valid data raised ValueError")
    
        try:
            self.new_datacube.init_var("AvgLandTemp", 8)
            self.new_datacube.init_var([], "c")
            self.new_datacube.init_var(10, 10)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_main_subset(self):
        self.new_datacube.init_var("AvgLandTemp", "c")
        self.new_datacube.init_var("AvgTemperatureColor", "d")
        self.new_datacube.init_var("AvgLandTemp", "variable")
        try:
            self.new_datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.main_subset('$d', 'Lat(53.08), Long(8.80)')
            self.new_datacube.main_subset('$variable', 'ansi("2014-01":"2014-12")')
            expected_variables = ["$c", "$d", "$variable"]
            expected_subsets = ['Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")', 'Lat(53.08), Long(8.80)', 'ansi("2014-01":"2014-12")']
            self.assertEqual(expected_variables, self.new_datacube.d_query_vars)
            self.assertEqual(expected_subsets, self.new_datacube.d_main_operations)
        except ValueError:
            self.fail("Valid data raised ValueError")
  
        try: 
            self.new_datacube.main_subset('c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.main_subset('variable', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
            
        try:
            self.new_datacube.main_subset(10, 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.main_subset('$variable', ['Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")'])
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_reset(self):
        self.new_datacube.init_var("AvgLandTemp", "c")
        self.new_datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
        self.new_datacube.d_agg_func = "min"
        self.new_datacube.d_encoding_type = "csv"
        try:
            self.new_datacube.reset()
            self.assertEqual(self.new_datacube.d_main_operations, [])
            self.assertEqual(self.new_datacube.d_coverages, [])
            self.assertEqual(self.new_datacube.d_query_vars, [])
            self.assertEqual(self.new_datacube.d_agg_func, None)
            self.assertEqual(self.new_datacube.d_encoding_type, '')
        except ValueError:
            self.fail("Valid data raised ValueError")
        
    def test_clear_data(self):
        self.new_datacube.init_var("AvgLandTemp", "c")
        self.new_datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
        self.new_datacube.init_var("AvgTemperatureColor", "d")
        self.new_datacube.main_subset('$d', 'ansi("2014-01":"2014-12")')
        try:
            self.new_datacube.clear_var_data("$c")
            self.assertEqual(self.new_datacube.d_main_operations, ['ansi("2014-01":"2014-12")'])
            self.assertEqual(self.new_datacube.d_coverages, ["AvgTemperatureColor"])
            self.assertEqual(self.new_datacube.d_query_vars, ["$d"])
        except ValueError:
            self.fail("Valid data raised ValueError")
            
        try: 
            self.new_datacube.clear_var_data('c')
            self.new_datacube.clear_var_data('$variable')
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
            
        try:
            self.new_datacube.clear_var_data(10, 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_d_encoding(self):
        try:
            self.new_datacube.d_encoding("csv")
            self.new_datacube.d_encoding("png")
            self.assertEqual("image/png", self.new_datacube.d_encoding_type)
        except ValueError:
            self.fail("Valid data raised ValueError")
            
        try: 
            self.new_datacube.d_encoding("type")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
            
        try:
            self.new_datacube.d_encoding(10)
            self.new_datacube.d_encoding([])
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_d_aggregate(self):
        try:
            self.new_datacube.init_var("AvgLandTemp", "c")
            self.new_datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.d_aggregate("min", "$c > 20")
        except ValueError:
            self.fail("Valid data raised ValueError")
            
        try: 
            self.new_datacube.d_aggregate("abs", "$c")
            self.new_datacube.d_aggregate("abs", "$type")
            self.new_datacube.d_aggregate("min", "$variable")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
            
        try:
            self.new_datacube.d_aggregate("min", 10)
            self.new_datacube.d_aggregate([], "$c > 20")
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_combination_complex_query(self):
        try:
            self.new_datacube.init_var("AvgLandTemp", "c")
            self.new_datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.init_var("AvgLandTemp", "d")
            self.new_datacube.main_subset('$d', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.combination_complex_query("$c + 3*$c")
            self.new_datacube.combination_complex_query("($c + $d - 20) > 20")
        except ValueError:
            self.fail("Valid data raised ValueError")
            
        try: 
            self.new_datacube.combination_complex_query("$var + $c")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
            
        try:
            self.new_datacube.combination_complex_query([("$c + $d")])
            self.new_datacube.combination_complex_query(10)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_replace_vars(self):
        try: 
            self.new_datacube.init_var("AvgLandTemp", "c")
            self.new_datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.init_var("AvgLandTemp", "d")
            self.new_datacube.main_subset('$d', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.replace_vars()
            self.new_datacube.replace_vars("$c + $d", "$c")
            self.new_datacube.replace_vars("$c + $d")
        except ValueError:
            self.fail("Valid data raised ValueError") 
            
        try: 
            self.new_datacube.replace_vars("$var + $c")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
            
        try:
            self.new_datacube.replace_vars([("$c + $d")], "$c")
            self.new_datacube.replace_vars(10, "$c")
            self.new_datacube.replace_vars("$c", 10)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_d_execute(self):
        try: 
            self.new_datacube.init_var("AvgLandTemp", "c")
            self.new_datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.init_var("AvgLandTemp", "d")
            self.new_datacube.main_subset('$d', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
            self.new_datacube.d_execute("$c")
            self.new_datacube.d_aggregate("min", "$c > 30")
            self.new_datacube.d_execute()
            self.new_datacube.d_agg_func = None
            self.new_datacube.combination_complex_query("$c + $d")
            self.new_datacube.d_encoding("csv")
        except ValueError:
            self.fail("Valid data raised ValueError") 
            
        try: 
            self.new_datacube.d_execute("$variable")
        except ValueError:
            pass
        else:
            self.fail("Expected ValueError was not raised")  
            
        try:
            self.new_datacube.d_execute(["$c"])
            self.new_datacube.d_execute(10)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError was not raised")
            
    def test_nir_green_red_ratio_query(self):
        try:
            query = self.datacube.nir_green_red_ratio(self.coverage_var)
            # Assert that the query is constructed properly
            self.assertIsInstance(query, str)
            self.assertNotEqual(query, "")  # Checking if the query is not empty
        except Exception as e:
            self.fail(f"NIR Green Red Ratio query construction failed with error: {e}")

    def test_d_execute_nir_green_red_ratio(self):
        try:
            response, query = self.datacube.d_execute_nir_green_red_ratio(self.coverage_var)
            # Assert that the response and query are not empty
            self.assertIsNotNone(response)
            self.assertIsNotNone(query)
            self.assertIsInstance(query, str)

            # Check if the response is a non-empty byte string (binary data)
            self.assertIsInstance(response, bytes)
            self.assertGreater(len(response), 0)

            # saving the image to a file for manual inspection
            with open("nir_green_red_ratio_test_image.jpg", "wb") as f:
                f.write(response)

        except Exception as e:
            self.fail(f"NIR Green Red Ratio execution failed with error: {e}")

    def test_sobel_query(self):
        try:
            query = self.datacube.sobel_edge_detection_query(self.coverage_var)
            # Assert that the query is constructed properly
            self.assertIsInstance(query, str)
            self.assertNotEqual(query, "")  # Check if the query is not empty
        except Exception as e:
            self.fail(f"Sobel query construction failed with error: {e}")

    def test_d_execute_sobel(self):
        try:
            response, query = self.datacube.d_execute_sobel(self.coverage_var)
            # Assert that the response and query are not empty
            self.assertIsNotNone(response)
            self.assertIsNotNone(query)
            self.assertIsInstance(query, str)

            # Check if the response is a non-empty byte string (binary data)
            self.assertIsInstance(response, bytes)
            self.assertGreater(len(response), 0)

            #  # saving the image to a file for manual inspectionion
            with open("sobel_test_image.jpg", "wb") as f:
                f.write(response)

        except Exception as e:
            self.fail(f"Sobel execution failed with error: {e}")
        
if __name__ == "__main__":
    unittest.main()

try:
    from src.datacube import DatacubeObject
    from src.database_connection import DatabaseConnectionObject
except Exception as e:
    print("Import error in dc_example.py.")
    print("Make sure you're running the command in the parent directory")

def main():
    server_url = "https://ows.rasdaman.org/rasdaman/ows"
    cvg_url = "https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities"
    dbc = DatabaseConnectionObject(server_url, cvg_url)
    
    datacube = DatacubeObject(dbc)
    datacube.init_var("AvgLandTemp", "c")
    datacube.main_subset('$c', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
    datacube.init_var("AvgLandTemp", "d")
    datacube.main_subset('$d', 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
    datacube.combination_complex_query("$c + 3*$d")
    print(datacube.d_execute()[0])
    datacube.d_aggregate("min", "($d + $c) > 20")
    print(datacube.d_execute())

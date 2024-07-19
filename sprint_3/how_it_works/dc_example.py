try:
    from src.datacube import DatacubeObject
    from src.database_connection import DatabaseConnectionObject
except Exception as e:
    print("Import error in dc_example.py.")
    print("Make sure you're running the command in the parent directory")

"""
how to run: 'python -m src.dbc_example',
while being situated in the parent directory of both src and how_it_works.
"""

def main():
    server_url = "https://ows.rasdaman.org/rasdaman/ows"
    cvg_url = "https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities"
    dbc = DatabaseConnectionObject(server_url, cvg_url)

    datacube = DatacubeObject(dbc, "AvgLandTemp")
    datacube.check_lat(-90)
    result = datacube.subset("Lat", "53:55").subset("Long", "90:92").timerange("2014-03", "2014-12").aggregate("max", ">=", 10).execute()
    print(result[1])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(f"Interrupted...")
    except Exception as e:
        print(f"An error occured: {e}")

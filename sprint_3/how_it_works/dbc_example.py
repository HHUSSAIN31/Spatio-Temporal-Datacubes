try:
    from src.database_connection import DatabaseConnectionObject
except Exception as e:
    print("Import error in dbc_example.py.")
    print("Make sure you're running the command in the parent directory")

"""
how to run: 'python -m src.dbc_example',
while being situated in the parent directory of both src and how_it_works.
"""

def main():
    dbc = DatabaseConnectionObject("https://ows.rasdaman.org/rasdaman/ows", "https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities")
    if dbc.pre_processed_coverage_support:
        print("id: S2_L2A_32631_B01_60m")
        print(dbc.pre_processed_coverage_dict['S2_L2A_32631_B01_60m'].extracted_bounds_dict['date'])
        print(dbc.pre_processed_coverage_dict['S2_L2A_32631_B01_60m'].extracted_bounds_dict['coord_1'])
        print(dbc.pre_processed_coverage_dict['S2_L2A_32631_B01_60m'].extracted_bounds_dict['coord_2'])

        print()

        print("id: AvgLandTemp")
        print(dbc.pre_processed_coverage_dict['AvgLandTemp'].extracted_bounds_dict['date'])
        print(dbc.pre_processed_coverage_dict['AvgLandTemp'].extracted_bounds_dict['coord_1'])
        print(dbc.pre_processed_coverage_dict['AvgLandTemp'].extracted_bounds_dict['coord_2'])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(f"Interrupted...")
    except Exception as e:
        print(f"An error occured: {e}")

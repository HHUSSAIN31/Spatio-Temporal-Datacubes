
from database_connection import DatabaseConnectionObject
from datacube import DatacubeObject

def main():
    server_url = "https://ows.rasdaman.org/rasdaman/ows"

    # Creating an instance of DatabaseConnectionObject
    dbc = DatabaseConnectionObject(server_url)

    try:
        # Establish connection to the server
        dbc.establish_connection()

        # Create a DatacubeObject for a specific coverage
        coverage_name = "my_coverage"
        datacube = DatacubeObject(dbc, coverage_name)

        # Perform datacube operations
        # Example: Subset and aggregate operations
        result = datacube['axis0':0, 'axis1':100].aggregate('mean').execute()

        if result is not None:
            print("Query executed successfully. Received response:")
            print(result)
        else:
            print("Error executing query.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

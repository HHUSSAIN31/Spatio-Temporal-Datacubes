# Create a connection to the WCPS server
from src.database_connection import DatabaseConnectionObject
from src.datacube import DatacubeObject

server_url = "https://ows.rasdaman.org/rasdaman/ows"
cvg_url = "https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities"
dbc = DatabaseConnectionObject(server_url, cvg_url)

# Initialize a datacube object
datacube = DatacubeObject(dbc, "AvgLandTemp")

# Build and execute a query
result = datacube\
    .subset("Lat", "0:10") \
    .subset("Long", "20:30") \
    .aggregate("avg") \
    .execute()

# Handle the result
if result:
    print("Query executed and data retrieved successfully.")
    print(result[0])
    # Further processing here
else:
    print("Query failed or returned no data.")

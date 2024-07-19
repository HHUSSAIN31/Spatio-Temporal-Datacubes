# Create a connection to the WCPS server
from sprint_1.src.database_connection import DatabaseConnectionObject
from sprint_1.src.datacube import DatacubeObject

server_url = "https://ows.rasdaman.org/rasdaman/ows"
dbc = DatabaseConnectionObject(server_url)
dbc.establish_connection()

# Initialize a datacube object
datacube = DatacubeObject(dbc, "MODIS_Land_Surface_Temp")

# Build and execute a query
result = datacube \
    .subset("Lat", "0:10") \
    .subset("Long", "20:30") \
    .add_condition("temperature > 300") \
    .aggregate("avg(temperature)") \
    .execute()

# Handle the result
if result:
    print("Query executed and data retrieved successfully.")
    # Further processing here
else:
    print("Query failed or returned no data.")

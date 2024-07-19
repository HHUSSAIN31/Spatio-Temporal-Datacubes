from dbc import DatabaseConnection
from datacube.dco import Datacube

# Initialize the Datacube object
dc_object = Datacube(dbc)

# Define test parameters
region = 'Germany'
time_range = "2014-07"

# Generate WCPS query
query = dc_object.std_deviation("Temperature", region, time_range)

# Define expected query
expected_query = f"""
for $c in (Temperature_{region})
return
    stddev($c[ansi("{time_range}")])
"""

# Perform assertion
assert query.strip() == expected_query.strip(), "Test Case Failed"
print("'std_deviation' function Test Case Passed\n")

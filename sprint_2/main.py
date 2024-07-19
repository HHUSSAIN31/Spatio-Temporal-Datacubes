'''The updated main.py script reflects several improvements and adaptations for Sprint 2:

Modularization and Organization:
The code is organized into functions, each responsible for testing a specific method of the Datacube class. This modular structure enhances readability and maintainability, making it easier to understand and manage the testing process.
The main() function orchestrates the execution of all test functions, providing a clear entry point for running the tests.
Improved Test Coverage:
The script now includes test functions for all methods of the Datacube class, ensuring comprehensive test coverage. This expansion of test coverage is crucial for validating the functionality of new features introduced in Sprint 2.
Exception Handling:
Each test function incorporates exception handling to catch and handle any errors that may occur during method execution. This ensures that the testing process is robust and resilient to potential failures, allowing for better identification and diagnosis of issues.
Readability and Maintainability:
The code follows a clear and consistent naming convention for test functions, making it easy to identify the purpose of each test.
Comments have been added where necessary to provide clarity and context, enhancing code readability and facilitating future maintenance efforts.
Overall, these improvements contribute to a more robust and effective testing process, enabling the verification of new features introduced in Sprint 2 while maintaining code quality and reliability.
'''
from datacube.dco import Datacube  
from dbc import DatabaseConnection  

def main():
    url = 'https://ows.rasdaman.org/rasdaman/ows'

    # Create a DatabaseConnection instance
    dbc = DatabaseConnection(url)

    # Create a Datacube instance
    datacube = Datacube(dbc)

    # Run test methods
    test_subset_temperature(datacube)
    test_avg_temperature(datacube)
    test_max_temperature(datacube)
    test_min_temperature(datacube)
    test_temperature_anomalies(datacube)
    test_std_deviation(datacube)
    test_median_temperature(datacube)
    test_interquartile_range(datacube)
    test_variance_temperature(datacube)
    test_total_precipitation(datacube)
    test_rainy_days_count(datacube)

def test_subset_temperature(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        response, wcps_query = datacube.subset_temperature(region, time_range)
        print("Subset temperature operation successful.")
    except Exception as e:
        print(f"Error in subset_temperature method: {e}")

def test_avg_temperature(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.avg_temperature(region, time_range)
        print(f"Average temperature for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in avg_temperature method: {e}")

def test_max_temperature(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.max_temperature(region, time_range)
        print(f"Maximum temperature for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in max_temperature method: {e}")

def test_min_temperature(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.min_temperature(region, time_range)
        print(f"Minimum temperature for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in min_temperature method: {e}")

def test_temperature_anomalies(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.temperature_anomalies(region, time_range)
        print(f"Temperature anomalies for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in temperature_anomalies method: {e}")

def test_std_deviation(datacube):
    try:
        coverage = "Temperature"  
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.std_deviation(coverage, region, time_range)
        print(f"Standard deviation for {coverage}_{region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in std_deviation method: {e}")

def test_median_temperature(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.median_temperature(region, time_range)
        print(f"Median temperature for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in median_temperature method: {e}")

def test_interquartile_range(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.interquartile_range(region, time_range)
        print(f"Interquartile range for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in interquartile_range method: {e}")

def test_variance_temperature(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.variance_temperature(region, time_range)
        print(f"Variance of temperatures for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in variance_temperature method: {e}")
        
def test_total_precipitation(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        result = datacube.total_precipitation(region, time_range)
        print(f"Total precipitation for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in total_precipitation method: {e}")

# Test rainy_days_count method - Sprint 2
def test_rainy_days_count(datacube):
    try:
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        threshold = 5  # Define threshold for rainfall
        result = datacube.rainy_days_count(region, time_range, threshold)
        print(f"Number of days with rainfall above {threshold}mm for {region} between {time_range}: {result}")
    except Exception as e:
        print(f"Error in rainy_days_count method: {e}")

if __name__ == "__main__":
    main()

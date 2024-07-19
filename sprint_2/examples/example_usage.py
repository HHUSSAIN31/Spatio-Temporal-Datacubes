'''Example Usage File:
Purpose: An example usage file demonstrates how to use your project's functionality in a practical context.
Importance:
Provides a clear, real-world demonstration of how to interact with your project.
Helps users understand the intended usage and capabilities of your code.
Serves as a quick reference for developers to see the code in action without diving into implementation details.
Content:
Contains code snippets or scripts that demonstrate typical use cases of your project's features.
Includes comments or explanations to guide users through the examples.
Demonstrates how to instantiate objects, call methods, and handle common scenarios.'''
from sprint_2.datacube.dco import Datacube  
from dbc import DatabaseConnection  

def main():
    # URL of the WCPS server
    url = 'https://ows.rasdaman.org/rasdaman/ows'

    # Create a DatabaseConnection instance
    dbc = DatabaseConnection(url)

    # Create a Datacube instance
    datacube = Datacube(dbc)

    # Example usage of methods
    try:
        # Example usage of subset_temperature method
        region = "Germany"  
        time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]  
        response, wcps_query = datacube.subset_temperature(region, time_range)
        print("Subset temperature operation successful.")

        # Example usage of avg_temperature method
        result = datacube.avg_temperature(region, time_range)
        print(f"Average temperature for {region} between {time_range}: {result}")

        # Add more example usages of other methods here...

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

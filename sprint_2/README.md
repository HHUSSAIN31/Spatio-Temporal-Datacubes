# Software Engineering Project

### Sprint 1 Details:

The Datacube Operations Library is a Python package designed to interact with Web Coverage Processing Service (WCPS) servers. WCPS is a standard for querying and processing multi-dimensional raster data, commonly referred to as datacubes.

### Key Features:

These are the key features we have implemented during the first sprint:

1. **Subset Operations:**

   - The library allows users to extract subsets of data from a datacube based on spatial and temporal criteria. Users can specify the region of interest using latitude and longitude coordinates and define the time range for the subset.

2. **Statistical Calculations:**

   - We implemented statistical calculations on datacubes, including calculating averages, maximum and minimum values, and standard deviations. These calculations can be applied to specific regions and time ranges within the datacube.

3. **Temperature Anomalies:**

   - We also included functionality to compute temperature anomalies for specific regions and time ranges. This enables users to identify deviations from expected temperature patterns within the data.

4. **Connection Handling:**
   - Robust connection handling is implemented to ensure reliable communication with WCPS servers. Users can configure timeout durations and the number of retry attempts to accommodate varying network conditions.

### Usage:

1. **Initialization:**

   - Users initialize a `DatabaseConnection` object by providing the URL of the WCPS server. This object facilitates communication with the server and handles connection-related tasks.

2. **Datacube Operations:**

   - After initializing a `DatabaseConnection`, users create a `Datacube` object using the connection. This object serves as a container for performing operations on the datacube.
   - Operations such as subset extraction, statistical calculations, and anomaly detection are added to the `Datacube` object using its methods.

3. **Execution:**
   - Once operations are added, users generate a WCPS query string representing the desired operations. The library handles the execution of the query on the WCPS server and returns the results to the user.

This summary provides an overview of what we did during Sprint 1. It does not show any code.

### Sprint 2 Details:


### Description:

- The project is designed to facilitate analysis and visualization of geospatial data stored in a Web Coverage Processing Service (WCPS) server. It provides a Python interface for querying, retrieving, and analyzing data from the server, with a focus on climate and weather-related datasets.

---

** Key Features:**

1. **Datacube Class:**

   - Represents a datacube object that interacts with the WCPS server.
   - Allows users to perform various operations on the datacube, including subset queries, statistical calculations, and visualization.

2. **DatabaseConnection Class:**

   - Represents a connection to the WCPS server.
   - Handles the communication with the server and execution of queries.

3. **Subset Queries:**

   - Users can perform subset queries to retrieve specific portions of the datacube based on spatial and temporal criteria.

4. **Statistical Calculations:**

   - Users can calculate various statistical measures such as average, maximum, minimum, median, interquartile range, variance, standard deviation, total precipitation, and count of rainy days.

5. **Visualization:**

   - The library supports visualization of query results using PIL (Python Imaging Library) for image-based data.

6. **Error Handling:**

   - Comprehensive error handling mechanisms are implemented to provide informative error messages and handle various types of errors gracefully.

7. **Example Usages:**
   - Example scripts demonstrate how to use the library to perform common tasks such as querying data, calculating statistics, and visualizing results.

---

**Installation:**

```
pip install -r requirements.txt
```

---

**Usage:**

1. **Initialize Database Connection:**

   ```python
   from sprint_2.dbc import DatabaseConnection

   url = 'https://wcps-server-url'
   dbc = DatabaseConnection(url)
   ```

2. **Create Datacube Object:**

   ```python
   from sprint_2.datacube.dco import Datacube

   datacube = Datacube(dbc)
   ```

3. **Perform Operations:**

   ```python
   # Example: Subset Query
   region = "Germany"
   time_range = ["2024-01-01T00:00:00", "2024-12-31T23:59:59"]
   response, wcps_query = datacube.subset_temperature(region, time_range)
   ```

4. **Visualization:**

   ```python
   # Displaying the retrieved image
   img.show()
   ```

5. **Error Handling:**
   - Errors are raised with informative messages to assist in debugging.

---

**Testing:**

```
python -m unittest
```

---

**Contributing:**

1. Fork the repository
2. Create a new branch (`git checkout -b feature`)
3. Make changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature`)
5. Create a pull request



**Authors:**

- Ani Nikoladze-Janiashvili
- Haider Qaizar Hussain

1. **Additional Statistical Calculations:**

   - We expanded the range of statistical calculations available for datacubes, including median temperature, interquartile range, and variance of temperatures. These calculations provide deeper insights into the data's distribution and variability.

2. **Refactoring and Code Structure:**

   - We conducted meaningful refactoring to improve code readability, maintainability, and performance. This includes organizing code into modules, renaming variables for clarity, and optimizing algorithm efficiency.

3. **Enhanced Testing:**

   - We augmented the test suite with additional test cases to ensure comprehensive coverage of the library's functionality. These tests verify the correctness of methods and handle edge cases to improve robustness.

4. **Example Usage and Documentation:**
   - We provided example usage files to demonstrate how to utilize the library's features in real-world scenarios. Additionally, we enhanced the documentation to provide clear guidelines on installation, usage, and customization.

### Usage:

1. **Initialization:**

   - Users initialize a `DatabaseConnection` object by providing the URL of the WCPS server. This object facilitates communication with the server and handles connection-related tasks.

2. **Datacube Operations:**

   - After initializing a `DatabaseConnection`, users create a `Datacube` object using the connection. This object serves as a container for performing operations on the datacube.
   - Operations such as subset extraction, statistical calculations, and anomaly detection are added to the `Datacube` object using its methods.

3. **Execution:**
   - Once operations are added, users generate a WCPS query string representing the desired operations. The library handles the execution of the query on the WCPS server and returns the results to the user.

This summary provides an overview of what we accomplished in Sprint 2, building upon the foundation laid in Sprint 1. It does not show any code.

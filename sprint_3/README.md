# SE Project: Sprint 3

This is the project documentation for Team 38.

## Table of Contents

1. [Introduction](#introduction)
2. [UML Diagram](#uml-diagram)
3. [API Documentation](#api-documentation)
   - [Class `DatabaseConnectionObject`](#class-DatabaseConnectionObject)
   - [Class `DatacubeObject`](#class-DatacubeObject)

## Introduction

The project aims to integrate Python operations with WCPS (Web Coverage Processing Service) for transparent WCPS query generation. The task involves using  Python's reflection and overloading capabilities to transmit operations to the server through WCPS. This is implemented using an object-oriented approach.

The project focuses on WCPS (Web Coverage Processing Service), a declarative query language similar to SQL but tailored for datacubes instead of tables. In standard terminology, a datacube is referred to as a "coverage" and comprises an array along with associated metadata. WCPS syntax resembles FLOWR expressions found in XML and JSON. Operations supported by WCPS include accessing, subsetting, processing, aggregating, fusing, and encoding datacubes.

The database connection object `DatabasedConnectionObject` makes the connection to the server, while the datacube object `DatacubeObject` serves as its Python counterpart. `DatacubeObject` is linked to the server through `DatabaseConnectionObject` and identifies datacubes via their names through an OGC WCS `DescribeCoverage` request.

When the connection is created the `DatabaseConnectionObject` class extracts metadata from the database regarding the different coverages. The data gets preprocessed and stored in a dictionary, which can be used to access the data for specific coverage names. We use this data to check the bounds of the different axises for the coverages.

The functionality of the datacube is based on method chaining, which allows for the creation of various WCPS queries. The data responses are filtered according to user input and method selection. 

The project's deliverables include:
- Python library `wdc` (WCPS Datacube)
- Implementation documentation including UML class diagrams
- User training material in the form of a Jupyter notebook
- A comprehensive suite of test cases
- Optimization  and performance enhancements using Makefiles
- Files that extract coverage data from the server
- Automatically created debug file

## UML Diagram

![UML Diagram](uml_image.png "UML Diagram")

## API Documentation

### Class `DatabaseConnectionObject`
Class for datacube connection and query

| Method                             | Description                                                                                                                    |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `__init__`                         | Initializes a DatabaseConnectionObject object.                                                                                 |
| `test_connection`                  | Tests connection to the DatabaseConnectionObject's server_url through a GET request.                                           |
| `execute_query`                    | Sends a POST request to the DatabaseConnectionObject's server_url with the data parameter set to {'query': query}.             |
| `__interpret_error_msg`            | Attemps to extract error message from the server's response message.                                                           |
| `__pre_processing_coverages`       | Attempts to process once and for all a dictionary with the keys as coverage IDs and with the content as their extracted data   |

## DatabaseConnectionObject Methods

### `__init__(self, server_url: str, coverage_url: str = None) -> None`
Initializes a DatabaseConnectionObject object.

#### Parameters
- `server_url` (str): The base URL of the server.
- `coverage_url` (str, optional): The URL for getting the coverage to be preprocessed.

#### Raises
- `ValueError`: If `server_url` is not a string.

### `test_connection(self, print_status_updates: bool = False) -> None`
Tests connection to the server URL through a GET request.

#### Parameters
- `print_status_updates` (bool, optional): If `True`, prints log messages.

#### Raises
- `Exception`: If the connection fails.

### `execute_query(self, query: str, print_status_updates: bool = False) -> str`
Sends a POST request to the server URL with the data parameter set to `{'query': query}`.

#### Parameters
- `query` (str): The query to be sent to the server.
- `print_status_updates` (bool, optional): If `True`, prints log messages.

#### Returns
- `str`: The raw response.

#### Raises
- `Exception`: If the query execution fails.

### `__interpret_error_msg(self, response_txt: str) -> str`
Attempts to extract an error message from the server's response message.

#### Parameters
- `response_txt` (str): The server's response as a string.

#### Returns
- `str`: The extracted message if successful, an empty string otherwise.

### `__pre_processing_coverages(self) -> None`
Attempts to process a dictionary with the keys as coverage IDs and with the content as their extracted data.

### Class `DatacubeObject`
Class for working with data cubes obtained from a remote data server using `DatacubeConnetionObject`.

| Method                             | Description                                                                                                 |
|------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `__init__`                         | Initialize a new DatacubeObject instance.                                                                   |
| `create_datacube`             |Create a datacube by executing a WCPS query and writing the result to a NetCDF file.                              |
| `check_lat`                   | Check if the given latitude is within the valid range for the coverage.                                          |
| `check_lon`                   | Check if the given longitude is within the valid range for the coverage.                                         |
| `check_years`                            | Checks the validity of user inputed dates.                                                            |
| `subset`                      | Add a subset operation for a specific dimension (Lat/Lon) and a range.                                           |
| `execute`                  | Generate and execute a WCPS query based on accumulated operations.                                                  |
| `add_condition`                      | Performs filtering operations using a specific condition (operator + value).                              |
| `aggregate`                  | Add an aggregation operation, such as mean, max, sum, etc.                                                        |
| `timerange`                      | Add a time range filter to the operations list.                                                               |
| `encode`                      | Set an encoding type for the data.                                                                               |
| `polygon`                       | Clips data within a polygonal area and creates either a csv or an image response based on its dimensions.      |
| `to_Kelvin`                     | Calculate the Kelvin value of a temperature.                                                                   |
| `color_switching`                        | Perform color switching based on temperature cases and RGB values.                                    |
| `__getitem__`                      | Overload the slicing operator to allow easier specification of subsetting operations.                       |
| `__str__`                     | Return a string representation of the current state of the datacube operations.                                  |
| `extract_variables`                     | Extract variables from a command string. operations.                                  |
| `var_existence`                     | Check if variables exist in the data cube.                                  |
| `init_var`                     | Initialize a new variable with its associated coverage name.                                  |
| `main_subset`                     | Set the main operation for a specific variable. Usually a subset operation that will then be associated with the respecive variable. This variable will always be replaced with its operation so that dynamic query building, addition of different results and coverages and creation of complex queries will be possible.                                  |
| `reset`                     | Reset the state of the data cube object.                                  |
| `clear_var_data`                     | Clear data associated with a specific variable.                                  |
| `d_encoding`                     | Set the encoding type for the data cube.                                  |
| `d_aggregate`                     |Apply an aggregate function to the data cube. It includes a dynamic configuration of the aggregated factors and also allows to specify a specific condition.                                  |
| `combine_complex_queries`                     | Apply a combination complex query to the data cube. This function makes it possible to         dynamically combine the results of different queries, combine results from different coverages and even apply extra functions to the results.                                  |
| `replace_vars`                     | Replace variables in a command with their corresponding subsets.                                  |
| `d_execute`                     | Execute the data cube operation and return the result.                                  |
| `sobel_edge_detection_query`                     | Constructs and returns the WCPS query for performing Sobel edge detection.                                  |
| `d_execute_sobel`                     | Executes a query to perform Sobel edge detection on a given coverage variable.                                  |
| `nir_green_red_ratio`                     | Constructs and returns the WCPS query for dynamic Query2.                                  |
| `d_execute_nir_green_red_ratio`                     | Executes a query to calculate the NIR (Near Infrared) to Green to Red ratio for a given coverage variable.                                  |


## DatacubeObjects Methods

### `__init__(self, dbc: DatabaseConnectionObject, coverage_name: str)`
Initializes a new DatacubeObject instance.

#### Parameters
- `dbc` (DatabaseConnectionObject): DatabaseConnectionObject that manages the connection to the WCPS server.
- `coverage_name` (str): The name of the coverage to perform operations on.

#### Local Variables
- `operations` (list): List of operations to be performed on the coverage. Contains the general axis operations.
- `aggregate_function` (str): Checks if an aggregate function has been applied to the datacube.
- `encode_type` (str): Type of encoding to be used when returning data from the datacube.
- `polygon_set` (str): Checks if the polygon function has been applied to the datacube.
- `color_cases` (list): List of color cases for color switching operations.
- `color_returns` (list): List of color returns for color switching operations.
- `extras` (list): Additional parameters or options for datacube operations. Contains the additional filtering operations.

#### Raises
- `TypeError`: If `dbc` is not an instance of DatabaseConnectionObject or if `coverage_name` is not a string.

### `create_datacube(self) -> Tuple[DatacubeObject, xr.Dataset]`
Creates a datacube by executing a WCPS query and writing the result to a NetCDF file.

#### Returns
- `Tuple[DatacubeObject, xr.Dataset]`: A tuple containing the current DatacubeObject instance and the created datacube as an xarray Dataset.

### `check_lat(self, lat: Union[int, float]) -> None`
Checks if the given latitude is within the valid range for the coverage.

#### Parameters
- `lat` (Union[int, float]): Latitude to be checked.

#### Raises
- `ValueError`: If the latitude is outside the valid range.
- `KeyError`: If the bounds cannot be checked.
- `TypeError`: If the type of `lat` is invalid.

### `check_lon(self, lon: Union[int, float]) -> None`
Checks if the given longitude is within the valid range for the coverage.

#### Parameters
- `lon` (Union[int, float]): Longitude to be checked.

#### Raises
- `ValueError`: If the longitude is outside the valid range.
- `KeyError`: If the bounds cannot be checked.
- `TypeError`: If the type of `lon` is invalid.

### `check_years(self, start_date: str, end_date: str = None) -> None`
Checks the validity of user-inputted dates.

#### Parameters
- `start_date` (str): Starting date from which data should be requested.
- `end_date` (str, optional): Ending date from which data should be requested.

#### Raises
- `KeyError`: If the bounds cannot be checked.
- `TypeError`: If `start_date` and `end_date` have invalid types.
- `ValueError`: If the dates are not in the correct format or out of order.

### `subset(self, dimension: str, range_str: Union[int, float, str]) -> DatacubeObject`
Adds a subset operation for a specific dimension (Lat/Lon) and a range.

#### Parameters
- `dimension` (str): The dimension on which to apply the subset.
- `range_str` (Union[int, float, str]): The range in the format "start:end" to subset the dimension.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `ValueError`: If the dimension string or range of latitude/longitude values are invalid.
- `TypeError`: If the provided parameters are of invalid data types.

### `execute(self) -> Tuple[Response, str]`
Generates and executes a WCPS query based on accumulated operations.

#### Returns
- `Tuple[Response, str]`: A tuple containing the response of the execution and the sent query.

#### Raises
- `TypeError`: If the provided argument is not of the correct type.

### `add_condition(self, operator: str, arg: Union[int, float]) -> DatacubeObject`
Performs filtering operations using a specific condition (operator + value).

#### Parameters
- `operator` (str): The type of operation to be performed.
- `arg` (Union[int, float]): A value to be used for the operation.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `ValueError`: If an invalid operator or argument is provided.
- `TypeError`: If the provided parameters are not of the correct types.

### `aggregate(self, agg: str, operator: Optional[str] = None, value: Optional[Union[int, float]] = None) -> DatacubeObject`
Adds an aggregation operation, such as mean, max, sum, etc.

#### Parameters
- `agg` (str): Indicates the aggregate operation to be applied.
- `operator` (Optional[str]): An arithmetic operator that can follow the aggregate function.
- `value` (Optional[Union[int, float]]): A numerical value which is used with the operator to filter the data.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `ValueError`: If `agg` is not a recognized aggregate function or the operator is invalid.
- `TypeError`: If the provided parameters are of invalid data types.

### `timerange(self, start: str, end: Optional[str] = None) -> DatacubeObject`
Adds a time range filter to the operations list.

#### Parameters
- `start` (str): The start date of the time range.
- `end` (Optional[str]): The end date of the time range.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `ValueError`: If start and end are invalid or out of bounds.
- `TypeError`: If the provided parameters have invalid data types.

### `encode(self, type: str) -> DatacubeObject`
Set an encoding type for the data.

#### Parameters
- `type` (str): Specifies the encoding type of the data.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `TypeError`: If the encoding type is of invalid data type.

### `polygon(self, coordinates: List[Tuple[Union[float, int], Union[float, int], Union[str, None]]]) -> DatacubeObject`
Clips data within a polygonal area and creates either a csv or an image response based on its dimensions.

#### Parameters
- `coordinates` (List[Tuple[Union[float, int], Union[float, int], Union[str, None]]]): A list of tuples of coordinates that define the polygon - tuples of size as big as the axis' number of the coverage.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `ValueError`: If the coordinates list and its elements are invalid or out of order.
- `TypeError`: If the provided parameters are of invalid data types.
- `NotImplementedError`: If a tuple of 1 pair or more than 3 is given.

### `to_Kelvin(self) -> DatacubeObject`
Calculate the Kelvin value of a temperature.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

### `color_switching(self, info: Dict[Union[int, float], List[Union[int, float]]]) -> DatacubeObject`
Perform color switching based on temperature cases and RGB values.

#### Parameters
- `info` (Dict[Union[int, float], List[Union[int, float]]]): Dictionary containing case temperature values and their corresponding RGB changes.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `ValueError`: If the provided dictionary is invalid.
- `TypeError`: If the provided parameters have invalid data types.

### `__getitem__(self, slices: Union[int, slice, Tuple[slice]]) -> DatacubeObject`
Overload the slicing operator to allow easier specification of subsetting operations.

#### Parameters
- `slices` (Union[int, slice, Tuple[slice]]): A tuple of slice objects representing ranges for each dimension.

#### Returns
- `DatacubeObject`: The modified DatacubeObject instance.

#### Raises
- `ValueError`: If the slice object is of an unsupported type.

### `__str__(self) -> str`
Return a string representation of the current state of the datacube operations.

#### Returns
- `str`: A string representation of the DatacubeObject instance.

***
### `Added new functionality to the datacube class. Another approach at generating dynamic queries, which also allows for the combination of different queries, combined data manipulation and also data combination and manipulation from various coverages. Also interesting dynamic queries for sobel edge detection and NIR calculation were added.`
***

### `extract_variables(self, command: str) -> List[str]`

Extract variables from a command string.

#### Parameters
- `command` (str): The command string to extract variables from.

#### Returns
- `List[str]`: A list of variables found in the command string.

#### Raises
- `TypeError`: If the input command is not a string.
- `ValueError`: If no variables are found in the command string.

### `var_existence(self, command: str) -> bool`

Check if variables exist in the data cube.

#### Parameters
- `command` (str): The command string containing variables to check.

#### Returns
- `bool`: True if all variables exist, False otherwise.

#### Raises
- `TypeError`: If the input command is not a string.
- `ValueError`: If any of the variables do not exist in the data cube.

### `init_var(self, coverage_name: str, variable: str) -> DatacubeObject`

Initialize a new variable with its associated coverage name.

#### Parameters
- `coverage_name` (str): The name of the coverage associated with the variable.
- `variable` (str): The name of the variable to be initialized.

#### Returns
- `DatacubeObject`: The instance of the class for method chaining.

#### Raises
- `TypeError`: If coverage_name or variable is not a string.

### `main_subset(self, var: str, command: str) -> DatacubeObject`

Set the main operation for a specific variable. Usually a subset operation that will then be associated with the respective variable. This variable will always be replaced with its operation so that dynamic query building, addition of different results and coverages, and creation of complex queries will be possible.

#### Parameters
- `var` (str): The variable to set the main operation for.
- `command` (str): The command string representing the main operation.

#### Returns
- `DatacubeObject`: The instance of the class for method chaining.

#### Raises
- `TypeError`: If var or command is not a string.
- `ValueError`: If var does not match the expected format or if it does not exist in the data cube.

### `reset(self) -> DatacubeObject`

Reset the state of the data cube object.

#### Returns
- `DatacubeObject`: The instance of the class for method chaining.

### `clear_var_data(self, var: str) -> DatacubeObject`

Clear data associated with a specific variable.

#### Parameters
- `var` (str): The variable for which to clear data.

#### Returns
- `DatacubeObject`: The instance of the class for method chaining.

#### Raises
- `TypeError`: If var is not a string.
- `ValueError`: If var does not match the expected format or if it does not exist in the data cube.

### `d_encoding(self, type: str) -> DatacubeObject`

Set the encoding type for the data cube.

#### Parameters
- `type` (str): The encoding type to set.

#### Returns
- `DatacubeObject`: The instance of the class for method chaining.

#### Raises
- `TypeError`: If type is not a string.
- `ValueError`: If the encoding type is not supported.

### `d_aggregate(self, agg: str, filter: str = None) -> Tuple[DatacubeObject, str]`

Apply an aggregate function to the data cube. It includes dynamic configuration of the aggregated factors and also allows specifying a specific condition.

#### Parameters
- `agg` (str): The aggregate function to apply.
- `filter` (str, optional): A filtering condition to apply before aggregation.

#### Returns
- `Tuple[DatacubeObject, str]`: A tuple containing the instance of the class for method chaining and the resulting aggregate function.

#### Raises
- `TypeError`: If agg or filter is not a string.
- `ValueError`: If agg is not one of "min", "max", "avg", "count", or "sum".

### `combination_complex_query(self, complex_command: str) -> DatacubeObject`

Apply a combination complex query to the data cube. This function makes it possible to dynamically combine the results of different queries, combine results from different coverages, and even apply extra functions to the results.

#### Parameters
- `complex_command` (str): The complex command to apply.

#### Returns
- `DatacubeObject`: The instance of the class for method chaining.

#### Raises
- `TypeError`: If complex_command is not a string.
- `ValueError`: If the specified complex_command contains variables that do not exist in the data cube.

### `replace_vars(self, command_used: str = None, specify_var: str = None) -> Tuple[str, str]`

Replace variables in a command with their corresponding subsets.

#### Parameters
- `command_used` (str, optional): The command string to use for replacing variables.
- `specify_var` (str, optional): The variable to specifically replace.

#### Returns
- `Tuple[str, str]`: A tuple containing two strings representing the replaced expressions.

#### Raises
- `TypeError`: If command_used or specify_var is not a string.
- `ValueError`: If specify_var does not exist in the data cube or if the provided command contains invalid variable references.

### `d_execute(self, specify_var: str = None) -> Tuple[Any, str]`

Execute the data cube operation and return the result.

#### Parameters
- `specify_var` (str, optional): The variable to specifically execute the operation on.

#### Returns
- `Tuple[Any, str]`: A tuple containing the response from the database and the executed WCPS query.

#### Raises
- `TypeError`: If specify_var is provided but not a string.

### `sobel_edge_detection_query(self, coverage_var: str, band: str = "red", x_range: Tuple[float, float] = (-1, 1), y_range: Tuple[float, float] = (-1, 1), cut_out: Optional[List[int]] = None, encoding: str = "image/jpeg") -> str`

Constructs and returns the WCPS query for performing Sobel edge detection.

#### Parameters
- `coverage_var` (str): The coverage variable to use in the query.
- `band` (str): The band to apply the Sobel filter on. Default is "red".
- `x_range` (Tuple[float, float]): The range of x values for the kernel. Default is (-1, 1).
- `y_range` (Tuple[float, float]): The range of y values for the kernel. Default is (-1, 1).
- `cut_out` (Optional[List[int]]): The cutout region as [i_min, i_max, j_min, j_max]. Default is [10, 900, 10, 800].
- `encoding` (str): The encoding type for the output. Default is "image/jpeg".

#### Returns
- `str`: The constructed WCPS query.

### `d_execute_sobel(self, coverage_var: str, band: str = "red", x_range: Tuple[float, float] = (-1, 1), y_range: Tuple[float, float] = (-1, 1), cut_out: Optional[List[int]] = None, encoding: str = "image/jpeg") -> Tuple[Any, str]`

Executes a query to perform Sobel edge detection on a given coverage variable.

#### Parameters
- `coverage_var` (str): The coverage variable to perform edge detection on.
- `band` (str, optional): The name of the band to use for edge detection. Defaults to "red".
- `x_range` (Tuple[float, float], optional): The range of x-axis Sobel filter. Defaults to (-1, 1).
- `y_range` (Tuple[float, float], optional): The range of y-axis Sobel filter. Defaults to (-1, 1).
- `cut_out` (str, optional): Specifies a sub-region to perform edge detection. Defaults to None.
- `encoding` (str, optional): The encoding format for the output. Defaults to "image/jpeg".

#### Returns
- `Tuple[Any, str]`: A tuple containing the response from the query execution and the query itself.

### `nir_green_red_ratio(self, coverage_var: str, red_band: str = "red", green_band: str = "green", threshold: float = 0, encoding: str = "jpeg") -> str`

Constructs and returns the WCPS query for dynamic Query2.

#### Parameters
- `coverage_var` (str): The coverage variable to use in the query.
- `red_band` (str): The band to use as the red band.
- `green_band` (str): The band to use as the green band.
- `threshold` (float): The threshold value for the NDVI calculation.
- `encoding` (str): The encoding type for the output.

#### Returns
- `str`: The constructed WCPS query.

### `d_execute_nir_green_red_ratio(self, coverage_var: str, red_band: str = "red", green_band: str = "green", threshold: float = 0, encoding: str = "jpeg") -> Tuple[Any, str]`

Executes a query to calculate the NIR (Near Infrared) to Green to Red ratio for a given coverage variable.

#### Parameters
- `coverage_var` (str): The coverage variable to calculate the ratio for.
- `red_band` (str, optional): The name of the red band. Defaults to "red".
- `green_band` (str, optional): The name of the green band. Defaults to "green".
- `threshold` (int, optional): Threshold value for filtering the data. Defaults to 0.
- `encoding` (str, optional): The encoding format for the output. Defaults to "jpeg".

#### Returns
- `Tuple[Any, str]`: A tuple containing the response from the query execution and the query itself.


### File `get_coverage.py`

### `formatText(string: str) -> str`
Formats a given string by eliminating every character until the first encountered '}' character.

#### Parameters
- `string` (str): The string to be formatted.

#### Returns
- str: The formatted string.

#### Raises
- `ValueError`: If a type other than `str` is given.

### `isBlank(string: str) -> bool`
Checks whether a string is empty (blank) or not.

#### Parameters
- `string` (str): The string to be checked.

#### Returns
- bool: `True` if the string is blank, `False` otherwise.

#### Raises
- `ValueError`: If a type other than `str` is given.

### `getAvailableRequests(url: str ="https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities", statusUpdates: bool = False) -> list`
Makes a GET request to the provided URL, expecting an XML response. Processes the response into a list of lists.

#### Parameters
- `url` (str): The server's URL from which to request coverages using a GET request.
- `statusUpdates` (bool): Boolean variable based on which extra status updates on the standard output will be shared.

#### Returns
- list: Processed server's response into a list of lists or an empty list if anything went wrong.

#### Raises
- `ValueError`: If the type of `url` is not `str` or the type of `statusUpdates` is not `bool`.

### `processedDataIntoList(url: str ="https://ows.rasdaman.org/rasdaman/ows?&SERVICE=WCS&ACCEPTVERSIONS=2.1.0&REQUEST=GetCapabilities", statusUpdates: bool = False) -> tuple[type_request, int]`
Requests and formats data into `type_request` objects from a certain URL based on its expected incoming format.

#### Parameters
- `url` (str): The server's URL from which to request coverages using a GET request.
- `statusUpdates` (bool): Boolean variable based on which extra status updates on the standard output will be shared.

#### Returns
- tuple[type_request, int]: Tuple containing processed requests and the number of ignored requests.

#### Raises
- `ValueError`: If the type of `url` is not `str` or the type of `statusUpdates` is not `bool` or `int`.

### Class `type_request`
A class to store request structured information. It has an initialization function `__init__` and full comparison support for ordering lists of `type_request` objects.

#### Parameters
- `id` (str): A string containing the id.
- `coverageType` (str): A string containing a coverage_type.
- `coverageTypeExt` (list): A list containing any additional coverage_type information.
- `bounds_1` (list): A list containing core bounds (usually lower).
- `bounds_2` (list): A list containing core bounds (usually upper).
- `additionalParams` (list): A list of lists of any additional parameters. It usually includes better-defined information about bounds by specifying their type.
- `service_endpoint` (str): A string containing the server's endpoint. Can be used for both debug and server_request creation.
- `serviceType` (str): A string containing the service_type of the possible request. With the purpose of supporting pre-processing requests / independent (class related) request creation.
- `serviceVersion` (str): A string containing the server's service_version.
- `request` (str): A string containing the actual request.
- `extracted_bounds_dict` (dict): A dictionary of a list containing extracted information of any successfully extracted bounds on the axis_list.
- `encode_format` (str): A string with the purpose of serving the above-mentioned functionality of generating the request. Containing a format, ex: "img/png".

#### Raises
- `ValueError`: If any of the parameter's types are wrongfully given.

##### Methods
- `__init__(...) -> None`: Initializes the object.
- `__str__(...) -> str`: Returns what to be printed when trying to print an object of this type.
- `__lt__(other) -> bool`: Implementation of comparison sign: '<'.
- `__le__(other) -> bool`: Implementation of comparison sign: '<='.
- `__gt__(other) -> bool`: Implementation of comparison sign: '>'.
- `__ge__(other) -> bool`: Implementation of comparison sign: '>='.
- `__eq__(other) -> bool`: Implementation of comparison sign: '=='.


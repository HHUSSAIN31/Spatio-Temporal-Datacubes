import xarray as xr
from datetime import datetime
from .database_connection import *

class DatacubeObject:
    """
    Class for working with data cubes obtained from a remote data server.
    """
    def __init__(self, dbc : DatabaseConnectionObject, coverage_name=None):
        """
        Initialize a new DatacubeObject instance.
 
        :param dbc (Database Connection Object): DatabaseConnectionObject that manages the connection to the WCPS server.
        :param coverage_name (str): The name of the coverage to perform operations on.

        Local variables:
            operations (list): List of operations to be performed on the coverage. Contains the general axis operations.
            aggregate_function (str): Checks if an aggregate function has been applied to the datacube.
            encode_type (str): Type of encoding to be used when returning data from the datacube.
            polygon_set (str): Checks if the polygon function has been applied to the datacube.
            color_cases (list): List of color cases for color switching operations.
            color_returns (list): List of color returns for color switching operations.
            extras (list): Additional parameters or options for datacube operations. Contains the additional filtering operations.
            d_main_operations (list): List of the main/subset operations associated to each variable.
            d_query_vars (list): List containing all extracted variables.
            d_coverages (list): List of the coverages associated to each variable.
            d_agg_func (str): The aggregate function that is used for a query.
            d_encoding_type (str): The encoding type used in the new method for generating dynamic queries.
            d_combination_query: The complex cobinated query that gets used for the execution.
        """

        #Check the parameters' data types
        if not isinstance(dbc,  DatabaseConnectionObject):
            raise TypeError("invalid dbc type, expected type: DatabaseConnectionObject.")
        if coverage_name and not isinstance(coverage_name, str):
            raise TypeError("invalid coverage_name type, expected type: str.")

        self.dbc = dbc
        self.coverage_name = coverage_name
        self.operations = []
        self.aggregate_function = None
        self.encode_type = None
        self.polygon_set = None
        self.color_cases = []
        self.color_returns = []
        self.extras = []

        #new parameters used for another method of generating dynamic queries
        self.d_main_operations = []
        self.d_query_vars = []
        self.d_coverages = []
        self.d_agg_func = None
        self.d_encoding_type = ''
        self.d_combination_query = None
        
    def create_datacube(self):
        """
        Create a datacube by executing a WCPS query and writing the result to a NetCDF file.

        :return A tuple containing the current DatacubeObject instance and the created datacube as an xarray Dataset.
        """
        #extract the data from the database
        extraction_query = f"""
                        for $c in ({self.coverage_name})
                        return encode($c, "netcdf")
                        """

        response = self.dbc.execute_query(extraction_query)

        #store the extracted data into a netcdf file
        filename = "datacube.nc"  
        with open(filename, "wb") as f:
            f.write(response.content) 

        #create a datacube using xarray and the extracted data
        if response.status_code == 200:
            datacube = xr.open_dataset("datacube.nc")
            return self, datacube

    def check_lat(self, lat):
        """
        Check if the given latitude is within the valid range for the coverage.

        :param lat (int): Latitude to be checked.

        :raises ValueError if the latitude is outside the valid range.
        :raises KeyError Exception if the bounds cannot be checked
        :raises TypeError if the type of lat is invalid
        """

        #Extract the corresponding values for the specific coverage which have been preprocessed while establishing the connection
        if self.dbc.pre_processed_coverage_support:
            try:
                lower_lat = self.dbc.pre_processed_coverage_dict[self.coverage_name].extracted_bounds_dict['coord_1'][0]
                upper_lat = self.dbc.pre_processed_coverage_dict[self.coverage_name].extracted_bounds_dict['coord_1'][1]
                lower_lat = float(lower_lat)
                upper_lat = float(upper_lat)
            except KeyError:
                raise Exception("Unable to check")
        
        #Checking parameters' data types
        if not isinstance(lat, (int, float)):
                raise TypeError("invalid lat type, expected type: int or float.")
        
        if lower_lat <= lat <= upper_lat:
            pass
        else:
            raise ValueError("The latitude is not in the valid range")
            
    def check_lon(self, lon):
        """
        Check if the given longitude is within the valid range for the coverage.

        :param lon (int): Longitude to be checked.

        :raises ValueError: If the longitude is outside the valid range.
        :raises KeyError Exception if the bounds cannot be checked
        :raises TypeError if the type of lon is invalid
        """

        #Extract the corresponding values for the specific coverage which have been preprocessed while establishing the connection
        if self.dbc.pre_processed_coverage_support:
            try:
                lower_lon = self.dbc.pre_processed_coverage_dict[self.coverage_name].extracted_bounds_dict['coord_2'][0]
                upper_lon = self.dbc.pre_processed_coverage_dict[self.coverage_name].extracted_bounds_dict['coord_2'][1]
                lower_lon = float(lower_lon)
                upper_lon = float(upper_lon)
            except KeyError:
                raise Exception("Unable to check")

            #Checking parameters' data types
            if not isinstance(lon, (int, float)):
                raise TypeError("invalid lon type, expected type: int or float.")

            if lower_lon <= lon <= upper_lon:
                pass
            else:
                raise ValueError("The longitude is not in the valid range")

    def check_years(self, start_date: str, end_date: str = None) -> None:
        """
        Checks the validity of user inputed dates.
        
        :param: start_date (str): starting date from which data should be requested.
        :param: end_date (str):  ending  date from which data should be requested.
        
        :raises KeyError Exception if the bounds cannot be checked
        :raises TypeError if start_date and end_date have invalid types
        :raises ValueError if the  dates are not in correct format or out of order
        """
        date_format = "%Y-%m-%d"
        
        if not end_date:
            end_date = start_date

        if self.dbc.pre_processed_coverage_support:
            try:    
                start_bound = self.dbc.pre_processed_coverage_dict[self.coverage_name].extracted_bounds_dict['date'][0]
                end_bound = self.dbc.pre_processed_coverage_dict[self.coverage_name].extracted_bounds_dict['date'][1]
            except KeyError:
                raise Exception("Unable to check")

        # checking parameters' data types
        if not isinstance(start_date, str):
            raise TypeError("invalid start_date type, expected type: str.")
        if not isinstance(end_date, str):
            raise TypeError("invalid end_date type, expected type: str.")

        try:
            # convert the string to a date object
            # add support for both type of accepted inputs: YYYY-MM and YYYY-MM-DD
            # raise any possible occuring error
            if len(start_bound) > len("yyyy-mm"):
                start_bound = datetime.strptime(start_bound, date_format).date()
            else:
                start_bound = datetime.strptime(start_bound + "-01", date_format).date()
            if len(end_bound) > len("yyyy-mm"):
                end_bound = datetime.strptime(end_bound, date_format).date()
            else:
                end_bound = datetime.strptime(end_bound + "-01", date_format).date()
            if len(start_date) > len("yyyy-mm"):
                start_date = datetime.strptime(start_date, date_format).date()
            else:
                start_date = datetime.strptime(start_date + "-01", date_format).date()
            if len(end_date) > len("yyyy-mm"):
                end_date = datetime.strptime(end_date, date_format).date()
            else:
                end_date = datetime.strptime(end_date + "-01", date_format).date()
        except Exception as e:
            raise ValueError(e)

        # raise invalid date combinations erros, if any
        if start_bound <= start_date <= end_bound:
            pass
        else:
            raise ValueError(f"The start date is not withing the allowed range: [{start_bound} : {end_bound}].")
        
        if start_bound <= end_date <= end_bound:
            pass
        else:
            raise ValueError(f"The  end  date is not withing the allowed range: [{start_bound} : {end_bound}].")
 
        if start_date > end_date:
            raise ValueError("Start date cannot be greater than end date.")

    def subset(self, dimension:str, range_str):
        """
        Add a subset operation for a specific dimension (Lat/Lon) and a range.

        :param dimension (str): The dimension on which to apply the subset, typically 'axis0', 'axis1', etc.
        :param range_str (int, float, str): The range in the format "start:end" to subset the dimension. Single (int, float) values are also accepted.
        
        :return: self to allow for method chaining.

        :raises ValueError if the dimension string or range of latitude/longitude values are invalid
        """

        #Check the parameters' types
        if not isinstance(dimension, str):
            raise TypeError("invalid dimension type, expected type: str.")
        if not isinstance(range_str, (int, float, str)):
            raise ValueError("invalid range_str type, expected type: str, float or int.")

        if dimension != "Lat" and dimension != "Long":
            raise ValueError("The dimension can only be Lat or Long specifying either the Latitude or Longitude dimensions")

        #for single values - check the corresponding dimension
        if isinstance(range_str, (float, int)):
            if dimension == "Lat":
                self.check_lat(range_str)
            elif dimension == "Long":
                self.check_lon(range_str)

        #for range of values - check the corresponding values one by one
        else:
            start, end = range_str.split(':')

            start = int(start)
            end = int(end)

            if dimension == "Lat":
                for i in range(start, end + 1): 
                    self.check_lat(i)
            elif dimension == "Long":
                for i in range(start, end + 1):
                    self.check_lon(i)

        self.operations.append(f"{dimension}({range_str})")
        return self 

    def execute(self):
        """
        Generate and execute a WCPS query based on accumulated operations.

        :param dbc (DatabaseConnectionObject): Provides the connection to the database.
        
        :return the response of the execution and the sent query

        :raises TypeError if the provided argument is not of the correct type.
        """

        #Contains the general operations related to the axis
        operations_str = ','.join(self.operations)
        #Contains the additional filtering operations
        if self.extras == []:
            extras_str = ""
        else:
            extras_str = ' '.join(self.extras)

        #Constructs specific queries depending on the applied functions
        if self.operations != []:
            if self.aggregate_function:
                query = f'''for $c in ({self.coverage_name}) return {self.aggregate_function}($c[{operations_str}]{extras_str})'''
            elif self.encode_type:
                query = f'''for $c in ({self.coverage_name}) return encode($c[{operations_str}]{extras_str}, "{self.encode_type}")'''
            elif self.color_cases != []:
                query = f'''for $c in ({self.coverage_name}) \nreturn encode(\n\tswitch
                    case $c[{operations_str}] = 99999 return {{red: 255; green: 255; blue: 255}}\n'''    
                query += f'''\t\t{self.color_cases[0]} > $c[{operations_str}] {self.color_returns[0]}\n'''
                for i in range(1, len(self.color_cases)):
                    query += f'''\t\t{self.color_cases[i]} > $c[{operations_str}] {self.color_returns[i]}\n'''
                query += '''\t\tdefault return {red: 255; green: 0; blue: 0}, "image/png")'''
            else:
                query = f'''for $c in ({self.coverage_name}) return encode($c[{operations_str}]{extras_str}, "csv")'''
        else:
            if self.polygon_set:
                query = f'''for $c in ({self.coverage_name}) {self.polygon_set[0]} return encode (clip($c, $polygon), "{self.polygon_set[1]}")'''

        response = self.dbc.execute_query(query)
        return response, query
    
    def add_condition(self, operator:str, arg):
        '''
        Performs filtering operations using a specific condition (operator + value).
        
        :param operator (str):  The type of operation to be performed. 
        :param arg (int, float): A value to be used for the operation.
        
        :return self to allow for method chaining

        :raises  ValueError if an invalid operator or argument is provided.
        :raises TypeError if the provided parameters  are not of the correct types.
        '''

        #Check the parameters' data types
        if not isinstance(operator, str):
            raise TypeError("invalid operator type, expected type: str.")

        if not isinstance(arg, (int, float)):
            raise TypeError("invalid arg type, expected type: int or float.")

        operators = [">", ">=", "==", "<=", "<", "!=", "+", "-", "*", "/", "%"]
        if operator not in operators:
            raise ValueError("The provided operator is not valid.")
        
        #Add the operation to the list of extras
        self.extras.append(f"{operator} {arg}")
        
        return self

    def aggregate(self, agg: str, operator:str=None, value=None):
        """
        Add an aggregation operation, such as mean, max, sum, etc.

        :param agg (str): Indicates the aggregate operation to be applied
        :param operator (Optional[str]): An arithmetic operator that can follow the aggregate function.
        :param value  (Optional[float, int]): A numerical value which is used with the operator to filter the data.

        :return self to allow for method chaining

        :raise ValueError if `agg` is not a recognized aggregate function or the operator is invalid
        :raise TypeError if the provided parameters are of invalid data types
        """
        #Check the parameters' data types
        if not isinstance(agg, str):
            raise TypeError("invalid agg type, expected type: str.")
        if operator and not isinstance(operator, str):
            raise TypeError("invalid operator type, expected type: str.")
        if value and not isinstance(value, (int, float)):
            raise TypeError("invalid value type, expected type: int or float.")
        
        agg_operators = [">", ">=", "==", "<=", "<", "!="]

        #Check the aggregate function, the operator and the value
        if agg not in ["min", "max", "avg", "count", "sum"]:
            raise ValueError("Invalid aggregate function")
        
        if operator and operator not in agg_operators:
            raise ValueError("The provided operator is invalid for this aggregate function")

        #Aggregate specification to be used when building the query
        self.aggregate_function = agg

        #add the extra filtering operations
        if operator and value:
            self.extras.append(f"{operator} {value}")
        return self

    def timerange(self, start:str, end:str=None):
        '''
        Add a time range filter to the operations list.

        :param start (str): The start date of the time range.
        :param end (str): The end date of the time range.
        
        :return self to allow for method chaining

        :raises ValueError if start and end are invalid or out of bounds
        :raises TypeError if the provided parameters have invalid data types
        '''
        #Check the parameters' data types
        if not isinstance(start, str):
            raise TypeError("invalid start type, expected type: str.")
        if end and not isinstance(end, str):
            raise TypeError("invalid end type, expected type: str.")

        #Check the dates and if applicable add them to the operations list
        if start and end:
            self.check_years(start, end)
            self.operations.append(f"ansi(\"{start}\":\"{end}\")")
        elif end == None:
            self.check_years(start)
            self.operations.append(f"ansi(\"{start}\")")
        return self
    
    def encode(self, type: str):
        '''
        Set an encoding type for the data.

        :param type (str): Specifies the encoding type of the data.

        :return self to allow for method chaining

        :raises Type Error if the encoding type is of invalid data type
        '''

        #Check the encoding type and if applicable use it when building the query
        if not isinstance(type, str):
            raise TypeError("invalid encoding type value, expected type: str.")
        self.encode_type = type
        return self
    

    def polygon(self, coordinates: list):
        '''
        Clips data within a polygonal area and creates either a csv or an image response based on its dimensions.

        :param coordinates (list): A list of tuples of coordinates that define the polygon - tuples of size as big as the axis' number of the coverage.

        :return self to allow for method chaining

        raises ValueError if the coordinates list and its elements are invalid or out of order.
        raises TypeError if the provided parameters are of invalid data types.
        raises NotImplemented if a tuple of 1 pair or more than 3 is given.
        '''

        #Check the parameters' data types
        if not isinstance(coordinates, list):
            raise TypeError("invalid coordinates type, expected type: list.")

        #We cannot have a polygon of less than 3 coordinates
        if len(coordinates) < 3:
            raise ValueError("Polygon must have at least 3 coordinates")

        #Check the latitudes and longitudes
        if len(coordinates[0]) == 2:
            for lat, lon in coordinates:
                self.check_lat(lat)
                self.check_lon(lon)
            #Prepare a string to be used when building the query
            polygon_string = ", ".join([f"{lat} {lon}" for lat, lon in coordinates])
            self.polygon_set = f"let $polygon := POLYGON(({polygon_string}))", "image/png"
        elif len(coordinates[0]) == 3:
            for lat, lon, date in coordinates:
                self.check_lat(lat)
                self.check_lon(lon)
                self.check_years(date)
            #Prepare a string to be used when building the query
            polygon_string = ", ".join([f"\"{date}\" {lat} {lon}" for lat, lon, date in coordinates])
            self.polygon_set = f"let $polygon := POLYGON(({polygon_string}))", "csv"
        else:
            raise NotImplemented

        return self
    
    def to_Kelvin(self):
        '''
        Calculate the Kelvin value of a temperature.

        :return self to allow for method chaining
        '''
        
        self.extras.append(f"+ 273.15")
        return self    
    
    def color_switching(self, info: dict):
        '''
        Perform color switching based on temperature cases and RGB values.

        :param info (dict): Dictionary containing case temperature values and their corresponding rgb changes.

        :return self to allow for method chaining

        :raises ValueError if the provided dictionary is invalid
        :raises TypeError if the provided parameters have invalid data types
        '''

        #Check the parameters' data types
        if not isinstance(info, dict):
            raise TypeError("Invalid Input. Please provide a dictionary with temperature case values and rgb values")
        for keys, values in info.items():
            if len(values) < 3:
                raise ValueError("You need to specify three rgb values for red, green and blue")
            if not isinstance(keys, (int, float)):
                raise TypeError("The key should be a valid int or float value indicating a comparison temperature")
            for value in values:
                if not isinstance(value, (int, float)):
                    raise TypeError("The rgb value should be a valid int or float value")
        
        self.color_cases = []
        self.color_returns = []
        #Fill the lists to be used when building the query
        for keys, values in info.items():
            temp = f'''case {keys}'''
            self.color_cases.append(temp)
            red, green, blue = values
            temp = f'''return {{red: {red}; green: {green}; blue: {blue}}}'''
            self.color_returns.append(temp)
        return self

    def __getitem__(self, slices):
        """
        Overload the slicing operator to allow easier specification of subsetting operations.

        :param slices: A tuple of slice objects representing ranges for each dimension.
        :return: self to allow for method chaining.
        """
        if not isinstance(slices, tuple):
            slices = (slices,)

        for idx, slc in enumerate(slices):
            if isinstance(slc, slice):
                start = slc.start if slc.start is not None else ''
                end = slc.stop if slc.stop is not None else ''
                self.subset(f"axis{idx}", f"{start}:{end}")
            else:
                raise ValueError(f"Unsupported type for slicing: {type(slc)}. Expected 'slice' object.")

        return self

    def __str__(self):
        """
        Return a string representation of the current state of the datacube operations.
        """
        return f"DatacubeObject(coverage='{self.coverage_name}', operations={self.operations}, extras={self.extras})"

    '''
    ########Adding more dynamic functionality which allows for combining different results and even data from different coverages.########
    '''

    def extract_variables(self, command:str):
        '''
        Extract variables from a command string.

        :param command (str): The command string to extract variables from.

        :return list: A list of variables found in the command string.

        :raises TypeError: If the input command is not a string.
        :raises ValueError: If no variables are found in the command string.
        '''
        if not isinstance(command, str):
            raise TypeError("Invalid command type, expected type: str.")
        #The pattern used for finding variables
        pattern = r'\$[a-zA-Z_][a-zA-Z0-9_]*' 
        temp = re.findall(pattern, command)
        if temp:
            return temp
        else:
            raise ValueError("Invalid command - no variables found")

    def var_existence(self, command:str):
        '''
        Check if variables exist in the data cube.

        :param command (str): The command string containing variables to check.

        :return bool: True if all variables exist, False otherwise.

        :raises TypeError: If the input command is not a string.
        :raises ValueError: If any of the variables do not exist in the data cube.
        '''
        if not isinstance(command, str):
            raise TypeError("Invalid command type, expected type: str.")
        temp = self.extract_variables(command)
        #remove the repetitions and check if the variable has already been stored
        temp = set(temp)
        if temp.issubset(set(self.d_query_vars)):
            return True
        else:
            raise ValueError("The variables do not exist")
        
    def init_var(self, coverage_name:str, variable:str):
        '''
        Initialize a new variable with its associated coverage name.
        
        Example usage:
        datacube.init_var("AvgLandTemp", "d")

        :param coverage_name (str): The name of the coverage associated with the variable.
        :param variable (str): The name of the variable to be initialized.

        :return self: The instance of the class for method chaining.

        :raises TypeError: If coverage_name or variable is not a string.
        '''
        if not isinstance(coverage_name, str):
            raise TypeError("Invalid coverage_name type, expected type: str.")
        if not isinstance(variable, str):
            raise TypeError("Invalid variable type, expected type: str.")
        
        variable = "$" + variable
        self.d_query_vars.append(variable)

        while len(self.d_coverages) < len(self.d_query_vars):
            self.d_coverages.append(None)
        idx = self.d_query_vars.index(variable)
        self.d_coverages[idx] = coverage_name
        
        return self
    
    def main_subset(self, var, command):
        '''
        Set the main operation for a specific variable. Usually a subset operation that will then be associated with the respecive variable.
        This variable will always be replaced with its operation so that dynamic query building, addition of different results and coverages
        and creation of complex queries will be possible.
        
        Example usage: 
        datacube.init_var("AvgLandTemp", "d")
        datacube.main_subset('$d', 'Lat(40), Long(12), ansi("2012-01":"2012-12")')

        :param var (str): The variable to set the main operation for.
        :param command (str): The command string representing the main operation.

        :return self: The instance of the class for method chaining.

        :raises TypeError: If var or command is not a string.
        :raises ValueError: If var does not match the expected format or if it does not exist in the data cube.
        '''
        
        if not isinstance(command, str):
            raise TypeError( "Invalid command type, expected type: str.")
        if not isinstance(var, str):
            raise TypeError("Invalid var type, expected type: str.")
        if not re.match(r"\$[a-zA-Z_]\w*", var):
            raise ValueError("Invalid var format, expected pattern: '$*'.")

        while len(self.d_main_operations) < len(self.d_query_vars):
                self.d_main_operations.append(None)
        idx = self.d_query_vars.index(var)
        self.d_main_operations[idx] = command
        return self
    
    def reset(self):
        '''
        Reset the state of the data cube object.

        :return self: The instance of the class for method chaining.
        '''
        self.d_main_operations = []
        self.d_query_vars = []
        self.d_coverages = []
        self.d_agg_func = None
        self.d_encoding_type = ''
        return self
    
    def clear_var_data(self, var):
        '''
        Clear data associated with a specific variable.

        :param var (str): The variable for which to clear data.

        :return self: The instance of the class for method chaining.

        :raises TypeError: If var is not a string.
        :raises ValueError: If var does not match the expected format or if it does not exist in the data cube.
        '''
        if not isinstance(var, str):
            raise TypeError("Invalid var type, expected type: str.")
        if not re.match(r"\$[a-zA-Z_]\w*", var):
            raise ValueError("Invalid var format, expected pattern: '$*'.")
        if var not in self.d_query_vars:
            raise ValueError("The variable does not exist")
        idx = self.d_query_vars.index(var)
        del self.d_coverages[idx]
        del self.d_main_operations[idx]
        del self.d_query_vars[idx]
        return self

    def d_encoding(self, type):
        '''
        Set the encoding type for the data cube.
        
        Example usage:
        datacube.init_var("AvgLandTemp", "d")
        datacube.main_subset('$d', 'Lat(40), Long(12), ansi("2012-01":"2012-12")')
        datacube.d_encoding("csv")

        :param type (str): The encoding type to set.

        :return self: The instance of the class for method chaining.

        :raises TypeError: If type is not a string.
        :raises ValueError: If the encoding type is not supported.
        '''
        if not isinstance(type, str):
            raise TypeError("Invalid type type, expected type: str.")
        if type in ("csv", "text", "text/csv", "csv/text"):
            type = "csv"
        elif type in ("image", "png", "image/png", "png/image"):
            type = "image/png"
        elif type in ("application", "netcdf", "application/netcdf", "netcdf/application"):
            type = "application/netcdf"
        else:
            raise ValueError("Unsupported encoding type")
        self.d_encoding_type = type
        return self 

    def d_aggregate(self, agg, filter=None):
        '''
        Apply an aggregate function to the data cube. It includes a dynamic configuration of the aggregated factors and also
        allows to specify a specific condition.
        
        Example usage:
        datacube.aggregate(min, $c <= 90)
        datacube.d_aggregate("min", "($d + $c) > 20") - this works when the two variables are from the same coverage

        :param agg (str): The aggregate function to apply.
        :param filter (str, optional): A filtering condition to apply before aggregation.

        :return tuple: A tuple containing the instance of the class for method chaining and the resulting aggregate function.

        :raises TypeError: If agg or filter is not a string.
        :raises ValueError: If agg is not one of "min", "max", "avg", "count", or "sum".
        '''
        if not isinstance(agg, str):
            raise TypeError("Invalid agg type, expected type: str.")

        self.d_agg_func = agg
        temp_query = ''
        if agg not in ["min", "max", "avg", "count", "sum"]:
            raise ValueError("The aggregate operation is invalid")
        if filter != None:
            if not isinstance(filter, str):
                raise TypeError("The filtering condition needs to be a string")
            self.var_existence(filter)
            temp_query = self.replace_vars(filter)[1]
        else:
            temp_query = self.replace_vars()[1]
        self.d_agg_func = ''
        if agg == "min":
            self.d_agg_func = f"min({temp_query})"
        elif agg == "max":
            self.d_agg_func = f"max({temp_query})"
        elif agg == "avg":
            self.d_agg_func = f"avg({temp_query})"
        elif agg == "count":
            self.d_agg_func = f"count({temp_query})"
        elif agg == "sum":
            self.d_agg_func = f"sum({temp_query})"

        return self, self.d_agg_func

    def combination_complex_query(self, complex_command):
        '''
        Apply a combination complex query to the data cube. This function makes it possible to dynamically combine the results of different queries,
        combine results from different coverages and even apply extra functions to the results
        
        Example usage:             
        datacube.combination_complex_query("$c * 10 + $d-200")

        :param complex_command (str): The complex command to apply.

        :return self: The instance of the class for method chaining.

        :raises TypeError: If complex_command is not a string.
        :raises ValueError: If the specified complex_command contains variables that do not exist in the data cube.
        '''
        
        if not isinstance(complex_command, str):
            raise TypeError("Complex command needs to be a string.")
        self.var_existence(complex_command)
        self.d_combination_query = complex_command
        return self

    def replace_vars(self, command_used=None, specify_var=None):
        '''
        Replace variables in a command with their corresponding subsets.

        :param command_used (str, optional): The command string to use for replacing variables.
        :param specify_var (str, optional): The variable to specifically replace.

        :return tuple: A tuple containing two strings representing the replaced expressions.

        :raises TypeError: If command_used or specify_var is not a string.
        :raises ValueError: If specify_var does not exist in the data cube or if the provided command contains invalid variable references.
        '''
        expression1 = ''
        expression2 = ''
        if command_used and not isinstance(command_used, str):
            raise TypeError("Invalid command type. Expected type: str")
        if specify_var and not isinstance(specify_var, str):
            raise TypeError("Invalid variable type. Expected type: str")
        if command_used is not None:
            self.var_existence(command_used)
            expression2 = command_used
            #iterate over tuples of variables and corresponding subsets
            for i, (variable, com, cov) in enumerate(zip(self.d_query_vars, self.d_main_operations, self.d_coverages)):
                if specify_var and variable == specify_var:
                    expression1 += f'{variable} in ({cov})'
                    if com is not None:
                        #replace the variable in the expression with its subset
                        expression2 = expression2.replace(variable, f'{variable}[{com}]')
                elif not specify_var:
                    expression1 += f'{variable} in ({cov})'
                    if i < len(self.d_query_vars) - 1:  #Check if it's not the last iteration
                        expression1 += ', '
                    if com is not None:
                        #replace the variable in the expression with its subset
                        expression2 = expression2.replace(variable, f'{variable}[{com}]')
        else:
            for i, (variable, com, cov) in enumerate(zip(self.d_query_vars, self.d_main_operations, self.d_coverages)):
                if specify_var and variable == specify_var:
                    expression1 += f'{variable} in ({cov})'
                    if com is not None:
                        #replace the variable in the expression with its subset
                        expression2 = f'{variable} [{com}]'
                    else:
                        #if no subset exists, simply append the variable
                        expression2 += f'''{variable}'''
                    
                elif not specify_var:
                    expression1 += f'{variable} in ({cov})'
                    if i < len(self.d_query_vars) - 1:
                        expression1 += ', '
                    if com is not None:
                        #replace the variable in the expression with its subset
                        expression2 = f'{variable} [{com}]'
                    else:
                        #if no subset exists, simply append the variable
                        expression2 += f'''{variable}'''

        return expression1, expression2
        
    def d_execute(self, specify_var=None):
        '''
        Execute the data cube operation and return the result.
        
        Example usage:
        datacube.d_execute("$c")

        :param specify_var (str, optional): The variable to specifically execute the operation on.

        :return tuple: A tuple containing the response from the database and the executed WCPS query.

        :raises TypeError: If specify_var is provided but not a string.
        '''
        if specify_var and not isinstance(specify_var, str):
                raise TypeError("Invalid specify_var type. Expected: str")
        
        #check if the user has specified the variable for execution
        if specify_var:
            self.var_existence(specify_var)
        wcps_query = "for " 
        wcps_query += self.replace_vars(specify_var=specify_var)[0]

        wcps_query += " return "
        if self.d_agg_func:
            wcps_query += self.d_agg_func
            response = self.dbc.execute_query(wcps_query)
            return response, wcps_query    
        else:
            temp_query = ''
            if self.d_combination_query:
                temp_query = self.replace_vars(self.d_combination_query, specify_var=specify_var)[1]
            else:
                temp_query = self.replace_vars(specify_var=specify_var)[1]

            if self.d_encoding_type:
                wcps_query += f'''encode ({temp_query}, "{self.d_encoding_type}")'''
            else:
                wcps_query += f'''encode ({temp_query}, "csv")'''
            response = self.dbc.execute_query(wcps_query)
            return response, wcps_query
        
    def sobel_edge_detection_query(self, coverage_var, band="red", x_range=(-1, 1), y_range=(-1, 1), cut_out=None, encoding="image/jpeg"):
        """
        Constructs and returns the WCPS query for performing Sobel edge detection.

        Args:
            coverage_var (str): The coverage variable to use in the query.
            band (str): The band to apply the Sobel filter on. Default is "red".
            x_range (tuple): The range of x values for the kernel. Default is (-1, 1).
            y_range (tuple): The range of y values for the kernel. Default is (-1, 1).
            cut_out (list): The cutout region as [i_min, i_max, j_min, j_max]. Default is [10, 900, 10, 800].
            encoding (str): The encoding type for the output. Default is "image/jpeg".

        Returns:
            str: The constructed WCPS query.
        """
        if cut_out is None:
            cut_out = [10, 900, 10, 800]  # Default cutout if none is provided
        
        return f"""
        image>>for {coverage_var} in ({self.coverage_name})
        let $kernel1 := coverage kernel1
                        over $x x ({x_range[0]}:{x_range[1]}), $y y ({y_range[0]}:{y_range[1]})
                        value list < 1; 0; -1; 2; 0; -2; 1; 0; -1 >,
            $kernel2 := coverage kernel1
                        over $x x ({x_range[0]}:{x_range[1]}), $y y ({y_range[0]}:{y_range[1]})
                        value list < 1; 2; 1; 0; 0; 0; -1; -2; -1 >,
            $cutOut := [ i({cut_out[0]}:{cut_out[1]}), j({cut_out[2]}:{cut_out[3]}) ]
        return
            encode(
                sqrt(
                    pow(
                        coverage Gx
                        over $px1 i( imageCrsdomain( {coverage_var}[$cutOut], i ) ),
                            $py1 j( imageCrsdomain( {coverage_var}[$cutOut], j ) )
                        values
                            condense +
                            over $kx1 x( imageCrsdomain( $kernel1, x ) ),
                                $ky1 y( imageCrsdomain( $kernel1, y ) )
                            using $kernel1[ x($kx1), y($ky1) ] * {coverage_var}.{band}[ i($px1 + $kx1), j($py1 + $ky1) ] ,
                        2.0 )
                    +
                    pow(
                        coverage Gy
                        over $px2 i( imageCrsdomain( {coverage_var}[$cutOut], i ) ),
                            $py2 j( imageCrsdomain( {coverage_var}[$cutOut], j ) )
                        values
                            condense +
                            over $kx2 x( imageCrsdomain($kernel2, x ) ),
                                $ky2 y( imageCrsdomain($kernel2, y ) )
                            using $kernel2[ x($kx2), y($ky2) ] * {coverage_var}.{band}[ i($px2 + $kx2), j($py2 + $ky2) ] ,
                        2.0)
                    ) ,
                "{encoding}"
            )
        """

    def d_execute_sobel(self, coverage_var, band="red", x_range=(-1, 1), y_range=(-1, 1), cut_out=None, encoding="image/jpeg"):
        """
        Executes a query to perform Sobel edge detection on a given coverage variable.

        Args:
            coverage_var (str): The coverage variable to perform edge detection on.
            band (str, optional): The name of the band to use for edge detection. Defaults to "red".
            x_range (tuple, optional): The range of x-axis Sobel filter. Defaults to (-1, 1).
            y_range (tuple, optional): The range of y-axis Sobel filter. Defaults to (-1, 1).
            cut_out (str, optional): Specifies a sub-region to perform edge detection. Defaults to None.
            encoding (str, optional): The encoding format for the output. Defaults to "image/jpeg".

        Returns:
            tuple: A tuple containing the response from the query execution and the query itself.

        Example:
            response, query = d_execute_sobel("coverage_variable", band="red", x_range=(-1, 1), y_range=(-1, 1), cut_out=None, encoding="image/jpeg")
        """
        query = self.sobel_edge_detection_query(coverage_var, band, x_range, y_range, cut_out, encoding)
        response = self.dbc.execute_query(query)
        
        return response, query


    def  nir_green_red_ratio(self, coverage_var, red_band="red", green_band="green", threshold=0, encoding="jpeg"):
        """
        Constructs and returns the WCPS query for dynamic Query2.

        Args:
            coverage_var (str): The coverage variable to use in the query.
            red_band (str): The band to use as the red band.
            green_band (str): The band to use as the green band.
            threshold (float): The threshold value for the NDVI calculation.
            encoding (str): The encoding type for the output.

        Returns:
            str: The constructed WCPS query.
        """
        return f"""
        image>>for {coverage_var} in ({self.coverage_name}) return encode(
            (
                (
                    ({coverage_var}.{red_band} - {coverage_var}.{green_band}) / 
                    ({coverage_var}.{red_band} + {coverage_var}.{green_band})
                ) > {threshold}
            ) * 255
        , "{encoding}")
        """

    def d_execute_nir_green_red_ratio(self, coverage_var, red_band="red", green_band="green", threshold=0, encoding="jpeg"):
        """
        Executes a query to calculate the NIR (Near Infrared) to Green to Red ratio for a given coverage variable.

        Args:
            coverage_var (str): The coverage variable to calculate the ratio for.
            red_band (str, optional): The name of the red band. Defaults to "red".
            green_band (str, optional): The name of the green band. Defaults to "green".
            threshold (int, optional): Threshold value for filtering the data. Defaults to 0.
            encoding (str, optional): The encoding format for the output. Defaults to "jpeg".

        Returns:
            tuple: A tuple containing the response from the query execution and the query itself.

        Example:
            response, query = d_execute_nir_green_red_ratio("coverage_variable", red_band="red", green_band="green", threshold=50, encoding="jpeg")
        """
        query = self.nir_green_red_ratio(coverage_var, red_band, green_band, threshold, encoding)
        response = self.dbc.execute_query(query)
        return response, query

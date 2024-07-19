# DatacubeObject Class

The `DatacubeObject` class provides a flexible and chainable interface for interacting with a remote Web Coverage Processing Service (WCPS) server to manipulate and retrieve data from a specified coverage.

## Initialization

Upon instantiation of a `DatacubeObject`, the following parameters are provided:

- `dbc`: An instance of `DatabaseConnectionObject` managing the connection to the WCPS server.
- `coverage_name`: The name of the coverage on which operations will be performed.

## Supported Operations

### Subset Operation (`subset`)

- **Functionality**: Adds a subset operation for a specific dimension.
  
- **Parameters**:
  - `dimension`: The dimension (e.g., 'axis0', 'axis1') on which the subset is applied.
  - `range`: The range specified in the format "start:end" to subset the dimension.
  
- **Return Value**: Allows for method chaining.

### Execute Operation (`execute`)

- **Functionality**: Generates and executes a WCPS query based on accumulated operations.
  
- **Return Value**: Returns the response from the WCPS server or `None` if an error occurs.

### Conditional Filtering (`add_condition`)

- **Functionality**: Adds a conditional filtering operation to the query.
  
- **Parameters**:
  - `condition`: The condition to be applied.
  
- **Return Value**: Allows for method chaining.

### Aggregation Operation (`aggregate`)

- **Functionality**: Adds an aggregation operation (e.g., mean, max, sum) to the query.
  
- **Parameters**:
  - `operation`: The aggregation operation to be applied.
  
- **Return Value**: Allows for method chaining.

### Overloaded Indexing (`__getitem__`)

- **Functionality**: Overloads the slicing operator to enable easier specification of subsetting operations.
  
- **Parameters**:
  - `slices`: A tuple of slice objects representing ranges for each dimension.
  
- **Return Value**: Allows for method chaining.


wcps-python-integration/
│
├── src/                        
│   ├── __init__.py             
│   ├── database_connection.py  
│   └── datacube.py             
│
├── tests/                      
│   ├── __init__.py
│   ├── test_database_connection.py
│   └── test_datacube.py
│
├── docs/                       
│   └── ...
│
├── examples/                   
│   └── simple_usage.py
│
├── requirements.txt            
└── README.md                   

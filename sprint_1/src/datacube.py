class DatacubeObject:
    def __init__(self, dbc, coverage_name):
        """
        Initialize a new DatacubeObject instance.

        :param dbc: DatabaseConnectionObject that manages the connection to the WCPS server.
        :param coverage_name: The name of the coverage to perform operations on.
        """
        self.dbc = dbc
        self.coverage_name = coverage_name
        self.operations = []

    def subset(self, dimension, range):
        """
        Add a subset operation for a specific dimension.

        :param dimension: The dimension on which to apply the subset, typically 'axis0', 'axis1', etc.
        :param range: The range in the format "start:end" to subset the dimension.
        :return: self to allow for method chaining.
        """
        self.operations.append(f"{dimension}({range})")
        return self

    def execute(self):
        """
        Generate and execute a WCPS query based on accumulated operations.

        :return: The response from the WCPS server or None if an error occurred.
        """
        if not self.operations:
            print("No operations to execute.")
            return None

        # Generate the WCPS query string
        operations_str = ','.join(self.operations)
        query = f"for $c in ({self.coverage_name}) return encode($c[{operations_str}], 'image/jpeg')"

        # Execute the query via the DatabaseConnectionObject
        return self.dbc.execute_query(query)

    def add_condition(self, condition):
        """
        Add a conditional filtering operation to the query.
        """
        self.operations.append(f"{condition}")
        return self

    def aggregate(self, operation):
        """
        Add an aggregation operation, such as mean, max, sum, etc.
        """
        self.operations.append(f"{operation}")
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
        return f"DatacubeObject(coverage='{self.coverage_name}', operations={self.operations})"

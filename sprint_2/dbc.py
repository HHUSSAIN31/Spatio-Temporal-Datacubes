'''To accommodate custom query composition in the dbc.py module, 
we'll make minimal changes to the existing code.
 Since the DatabaseConnection class is primarily responsible for establishing a connection to the server, 
 it doesn't need significant modifications for custom query composition. 
 However, we can add a method to execute custom WCPS queries. 
 Here's the updated version of dbc.py:'''

import requests
import logging

class DatabaseConnection:
    def __init__(self, url, timeout=10, max_retries=3):
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)

        try:
            self._establish_connection()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to establish a connection to the server: {e}")

    def _establish_connection(self):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                response = requests.get(self.url, timeout=self.timeout)
                response.raise_for_status()  # Raise an exception for HTTP errors
                self.logger.info("Connection to the server established successfully!")
                return
            except requests.exceptions.RequestException as e:
                self.logger.warning("Connection attempt failed: %s", e)
                retry_count += 1
        raise ConnectionError(f"Failed to establish a connection after {self.max_retries} attempts")

    def execute_custom_query(self, wcps_query):
        """Execute custom WCPS query and return response."""
        try:
            response = requests.post(self.url, data={'query': wcps_query}, verify=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.content.decode()  # Decode the response content and return it
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error executing custom WCPS query: {e}")  # Raise a connection error if request fails

'''In this updated version, I've added the execute_custom_query method,
 which takes a custom WCPS query as input and executes it against the server.
   This method provides flexibility for users to compose and execute their own WCPS queries
   .'''



import requests
import re
from .get_coverage import processedDataIntoList

"""
how to run: 'python -m src.database_connection'
you need to be in sprint_2 (don't go to either src or get_coverage files)
"""

class DatabaseConnectionObject:
    def __init__(self, server_url : str, coverage_url: str = None) -> None:
        """
        Initializes a DatabaseConnectionObject object.

        :param server_url: a string with the server's base url.
        :param coverage_url: a string with the url for getting the coverage to be preprocessed.

        :raise: a ValueError if server_url is anything but a str variable.
                a ValueError if coverage_url is given and is anything by a str variable.
        """
        if not isinstance(server_url, str):
            raise ValueError("server_url gotta be a string.")
        if coverage_url != None:
            if not isinstance(coverage_url, str):
                raise ValueError("coverage_url gotta be a string.")
        
        self.server_url = server_url
        self.coverage_url = coverage_url
        self.pre_processed_coverage_support = False
        self.pre_processed_coverage_dict = None
        self.__pre_processing_coverages()

    def test_connection(self, print_status_updates: bool = False) -> None:
        """
        tests connection to the DatabaseConnectionObject's server_url through a GET request.
        
        :param print_status_updates: Prints on the standard output log messages if it's set to True.
        
        :raise: an exception if anything goes wrong.
        """
        try:
            if print_status_updates:
                print("Checking server availability:", end=' ')
            # Send a GET request to the server URL to establish connection
            response = requests.get(self.server_url)

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                if print_status_updates:
                    print("Connection established successfully.")
            else:
                if print_status_updates:
                    print(f"Connection failed, status code: {response.status_code}")
                raise Exception(f"bad response, status_code: {response.status_code}")

        # check whether the get function threw an error and handle it accordingly
        except requests.exceptions.RequestException as e:
            if print_status_updates:
                print(f"Error establishing connection: {e}")
                print("Check your Wi-Fi connection.")
            raise Exception(e)

    def execute_query(self, query : str, print_status_updates: bool = False) -> str:
        """
        sends a POST request to the DatabaseConnectionObject's server_url
        with the data parameter set to {'query': query}.
        
        :param query: query to be sent to the server.
        :param print_status_updates: Prints on the standard output log messages if it's set to True.
        :returns the content of the response.
        
        :raise: Exception error Will raise an exception is anything goes wrong.
        """
        try:
            # Send POST request to server_url
            response = requests.post(self.server_url, data = {'query': query})

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                if print_status_updates:
                    print("Request Made Successfully.")
                return response.content
            else:
                # if we got a different response code, we try to better understand the reason
                # based on server's response
                interpreted_error = self.__interpret_error_msg(response.text)
                if print_status_updates:
                    print(f"Query execution failure. Status code: {response.status_code}.")
                if interpreted_error != "":
                    raise Exception(f"bad response, status_code: {response.status_code}. "
                                    + interpreted_error)
                else:
                    raise Exception(f"bad response, status_code: {response.status_code}.")
        except requests.exceptions.RequestException as e:
            if print_status_updates:
                print(f"Error establishing connection: {e}")
            raise Exception(e)

    def __interpret_error_msg(self, response_txt: str) -> str:
        """
        Attemps to extract error message from the server's response message.

        :param response_text: server's response as a string.
        :return extracted message if the attempt succedes, empty string otherwise.
        """
        if isinstance(response_txt, str):
            # trying to find exception text in the server's response using a regex expression
            matched_errors = re.search(".*<.*ExceptionText>.*<.*ExceptionText>", response_txt)
            if matched_errors:
                # if something is found, it extracts its message content (without the tags)
                temp = response_txt[matched_errors.start():matched_errors.end()].strip()
                x = temp.find('>')
                y = len(temp) - temp[::-1].find('<')
                return temp[x+1:y-1]
            else:
                return ""
        else:
            return ""

    def __pre_processing_coverages(self):
        """
        Attempts to process once and for all a dictionary
        with the keys as coverage IDs and
        with the content as their extracted data.
        """
        if self.coverage_url == None:
            return
        try:
            lst, ignored = processedDataIntoList(self.coverage_url, False)
        except:
            return
        
        if ignored != 0 or lst == []:
            return
        
        try:
            dictionary = dict()
            for coverage in lst:
                dictionary[coverage.id] = coverage
        except:
            return
        
        self.pre_processed_coverage_support = True
        self.pre_processed_coverage_dict = dictionary

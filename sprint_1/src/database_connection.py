import requests


class DatabaseConnectionObject:
    def __init__(self, server_url):
        self.server_url = server_url

    def establish_connection(self):
        try:
            # Send a GET request to the server URL to establish connection
            response = requests.get(self.server_url)

            # Check if the response status code is 200 (OK)
            if response.status_code == 200:
                print("Connection established successfully.")
            else:
                print(f"Failed to establish connection. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error establishing connection: {e}")

# Usage example
# server_url = "https://ows.rasdaman.org/rasdaman/ows"
# dbc = DatabaseConnectionObject(server_url)
# dbc.establish_connection()
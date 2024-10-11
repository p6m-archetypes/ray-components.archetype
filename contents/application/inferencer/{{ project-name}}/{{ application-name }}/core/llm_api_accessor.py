import requests


class LlmApiAccessor:
    def __init__(self, base_url):
        """
        Initializes the Accessor with a base URL for the API.
        """
        self.base_url = base_url

    def get(self, endpoint, params=None):
        """
        Sends a GET request to a specified endpoint with optional parameters.

        :param endpoint: The API endpoint to append to the base URL.
        :param params: Optional dictionary of parameters to send with the request.
        :return: The response data as a Python dictionary if successful, None otherwise.
        """
        # Constructing the full URL
        url = f'{self.base_url}{endpoint}'

        # Sending the GET request
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an exception for 4XX/5XX errors

            # Assuming the response is JSON-formatted, return the parsed data
            return response.json()
        except requests.RequestException as e:
            # Handling exceptions (e.g., network issues, invalid response)
            print(f'An error occurred: {e}')
            return None

    def post(self, endpoint, data=None, json=None):
        """
        Sends a POST request to a specified endpoint with optional data or json.

        :param endpoint: The API endpoint to append to the base URL.
        :param data: Optional dictionary, bytes, or file-like object to send in the body of the request.
        :param json: Optional JSON data to send in the body of the request.
        :return: The response data as a Python dictionary if successful, None otherwise.
        """
        url = f'{self.base_url}{endpoint}'
        try:
            response = requests.post(url, data=data, json=json)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f'An error occurred: {e}')
            return None


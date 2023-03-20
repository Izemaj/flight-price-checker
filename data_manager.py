import requests
from pprint import pprint
class DataManager:
    """
    A class to manage the Google Sheet data.
    """
    def __init__(self) -> None:
        self.endpoint = "https://api.sheety.co/32f67aa8343d6984c3f94fba5340b51e/flightDeals/prices"
        self.response = requests.get(self.endpoint)
        self.data = self.response.json()["prices"]

    def update_iata(self, row_id, iata_code)-> None:
        """
        Updates the IATA code in the Google Sheet.

        Parameters:
            row_id (int): The row ID of the Google Sheet.
            iata_code (str): The IATA code of the city.

        Returns:
            None
        """
        url = f"{self.endpoint}/{row_id}"
        body = {
            "price":
            {"iataCode": iata_code}
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.put(url=url, json=body, headers=headers)
        print(response.text)
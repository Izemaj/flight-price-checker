import requests
from datetime import datetime

from flight_data import FlightData

class FlightSearch:
    """
    This class is responsible for talking to the Flight Search API.
    """
    def __init__(self) -> None:
        self.endpoint = "https://api.tequila.kiwi.com"
        self.api_key = "sr8YVF34A72RxohS4l9JMa6XPnnj3yDJ"

    def get_destination_code(self, city_name):
        """
        Returns the IATA code for a city.

        Parameters:
            city_name (str): The name of the city.

        Returns:
            str: The IATA code of the city.
        """
        print("Getting destination codes...")
        location_endpoint = f"{self.endpoint}/locations/query"
        headers = {"apikey": self.api_key}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        if response.json().get("locations") != None:
            results = response.json()["locations"]
            code = results[0]["code"]
            return code
        else:
            print(response.json())

    def check_flights(self, 
                      origin_city_code: str, 
                      destination_city_code: str, 
                      from_time: datetime, 
                      to_time: datetime) -> FlightData:
        """
        Returns flight data for a given city.
        
        Parameters:
            origin_city_code (str): The IATA code of the origin city.
            destination_city_code (str): The IATA code of the destination city.
            from_time (datetime): The earliest date to search for a flight.
            to_time (datetime): The latest date to search for a flight.
        
        Returns:
            FlightData: A FlightData object containing the flight data.
        """
        headers = {"apikey": self.api_key}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        search_endpoint = f"{self.endpoint}/v2/search"
        response = requests.get(search_endpoint, headers=headers, params=query)

        if response.json().get("data") != None:
            try:
                data =response.json()["data"][0]
                flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
                )
                return flight_data
            except IndexError:
                print(f"No flights found for {destination_city_code}.")
                return None
        else:
            print(response.json())

        

        
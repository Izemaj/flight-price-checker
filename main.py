from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta
import sys
import io

# Set output encoding to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

data_manager = DataManager()

sheet_data = data_manager.data
ORIGIN_CITY = "LON"
FROM_TIME = datetime.today() + timedelta(days=1)
TO_TIME = datetime.today() + timedelta(days=180)

for data in sheet_data:
    if not data["iataCode"]:
        data["iataCode"] = FlightSearch().get_destination_code(data["city"])
        data_manager.update_iata(data["id"], data["iataCode"])

    flight_search = FlightSearch()
    flights = flight_search.check_flights(ORIGIN_CITY, data["iataCode"], FROM_TIME, TO_TIME)

    if flights is not None and flights.price < data["lowestPrice"]:
      notificationManager = NotificationManager()
      message = f"Low price alert! Only £{flights.price} to fly from {flights.origin_city}-{flights.origin_airport} to {flights.destination_city}-{flights.destination_airport}, from {flights.out_date} to {flights.return_date}."
      notificationManager.send_sms(message)



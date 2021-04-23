import requests
from django.conf import settings


class AbstractAPI:

    def __init__(self):
        self.geolocation_api_key = settings.ABSTRACT_API_KEY
        self.holiday_api_key = settings.HOLIDAY_API_KEY

    def ip_geolocation(self):
        res = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={self.geolocation_api_key}")
        return res.json(), res.status_code

    def holidays(self, country, year, month, day):
        res = requests.get(
            f"https://holidays.abstractapi.com/v1/?"
            f"api_key={self.holiday_api_key}&country={country}&year={year}&month={month}&day={day}")
        return res.json(), res.status_code

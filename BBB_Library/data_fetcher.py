# data_fetcher.py
from abc import ABC, abstractmethod
import requests

class DataFetcher(ABC):
    @abstractmethod
    def fetch_data(self, query):
        """
        Fetches data based on a query.
        """
        pass

class GooglePlacesFetcher(DataFetcher):
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"

    def fetch_data(self, query):
        params = {'query': query, 'key': self.api_key}
        search_response = requests.get(self.search_url, params=params)
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data['status'] == 'OK':
                place_id = search_data['results'][0]['place_id']
                details_params = {'place_id': place_id, 'fields': 'name,formatted_address,formatted_phone_number,website', 'key': self.api_key}
                details_response = requests.get(self.details_url, params=details_params)
                if details_response.status_code == 200:
                    details_data = details_response.json()
                    return details_data['result'] if details_data['status'] == 'OK' else None
        return None
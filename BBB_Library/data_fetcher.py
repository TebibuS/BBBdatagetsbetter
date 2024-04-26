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
        # Construct the full URL for the search query
        search_url = f"{self.search_url}?query={query}&key={self.api_key}"

        try:
            search_response = requests.get(search_url)
            search_response.raise_for_status()  # Checks if the request was successful
            search_data = search_response.json()
            
            if search_data["status"] == "OK":
                # Assume the first result is the most relevant
                place_id = search_data["results"][0]["place_id"]
                
                # Prepare parameters for the details request
                details_params = {
                    "place_id": place_id,
                    "fields": "name,formatted_address,formatted_phone_number,website",
                    "key": self.api_key
                }
                details_response = requests.get(self.details_url, params=details_params)
                details_response.raise_for_status()  # Checks if the request was successful
                details_data = details_response.json()
                
                if details_data["status"] == "OK":
                    result = details_data["result"]
                    result['place_id'] = place_id  # Include place_id in the result
                    return result
                else:
                    print(f"Details API returned status: {details_data['status']}")
                    return None
            else:
                print(f"Search API returned status: {search_data['status']}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for query '{query}': {e}")
            return None

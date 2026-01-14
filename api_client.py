import requests
from config import Config


class AviationStackClient:

    def __init__(self, api_key: str = None):
        self.base_url = Config.BASE_URL
        self.api_key = api_key or Config.API_KEY
        self.session = requests.Session()
    
    def _build_params(self, **kwargs) -> dict:
        params = {"access_key": self.api_key}
        params.update({k: v for k, v in kwargs.items() if v is not None})
        return params
    
    def _make_get_request(self, endpoint: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        return response
    
    def get_flights(self, limit: int = None, offset: int = None, 
                    flight_status: str = None, dep_iata: str = None,
                    arr_iata: str = None, airline_iata: str = None,
                    flight_iata: str = None) -> requests.Response:
        # Get real-time flight data
        params = self._build_params(
            limit=limit,
            offset=offset,
            flight_status=flight_status,
            dep_iata=dep_iata,
            arr_iata=arr_iata,
            airline_iata=airline_iata,
            flight_iata=flight_iata
        )
        return self._make_get_request(Config.ENDPOINTS["flights"], params)
    
    def get_airports(self, limit: int = None, offset: int = None) -> requests.Response:
        # Get airports data
        params = self._build_params(limit=limit, offset=offset)
        return self._make_get_request(Config.ENDPOINTS["airports"], params)
    
    def get_airlines(self, limit: int = None, offset: int = None) -> requests.Response:
        # Get airlines data
        params = self._build_params(limit=limit, offset=offset)
        return self._make_get_request(Config.ENDPOINTS["airlines"], params)
    
    def get_airplanes(self, limit: int = None, offset: int = None) -> requests.Response:
        # Get airplanes data
        params = self._build_params(limit=limit, offset=offset)
        return self._make_get_request(Config.ENDPOINTS["airplanes"], params)
    
    def get_aircraft_types(self, limit: int = None, offset: int = None) -> requests.Response:
        # Get aircraft types data.
        params = self._build_params(limit=limit, offset=offset)
        return self._make_get_request(Config.ENDPOINTS["aircraft_types"], params)
    
    def get_countries(self, limit: int = None, offset: int = None) -> requests.Response:
        # Get countries data.
        params = self._build_params(limit=limit, offset=offset)
        return self._make_get_request(Config.ENDPOINTS["countries"], params)
    
    def get_endpoint(self, endpoint: str, **kwargs) -> requests.Response:
        # Generic method to call any endpoint.
        params = self._build_params(**kwargs)
        return self._make_get_request(endpoint, params)

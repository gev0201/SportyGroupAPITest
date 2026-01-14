import pytest
from config import Config


class TestAviationStackAPI:
    # Tests for AviationStack API.

    @pytest.mark.parametrize("endpoint,expected_keys", [
        (Config.ENDPOINTS["airports"], ["airport_name", "iata_code", "icao_code", "country_name"]),
        (Config.ENDPOINTS["airlines"], ["airline_name", "iata_code", "icao_code", "country_name"]),
        (Config.ENDPOINTS["airplanes"], ["registration_number", "iata_code_long", "model_name"]),
        (Config.ENDPOINTS["aircraft_types"], ["aircraft_name", "iata_code"]),
        (Config.ENDPOINTS["countries"], ["country_name", "country_iso2", "capital"]),
    ])
    def test_endpoint_returns_expected_data_structure(self, api_client, endpoint, expected_keys):
        # TC001
        response = api_client.get_endpoint(endpoint, limit=1)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        json_data = response.json()
        
        assert "pagination" in json_data, "Response should contain 'pagination' object"
        assert "data" in json_data, "Response should contain 'data' array"
        
        pagination = json_data["pagination"]
        assert "limit" in pagination, "Pagination should contain 'limit'"
        assert "offset" in pagination, "Pagination should contain 'offset'"
        assert "count" in pagination, "Pagination should contain 'count'"
        assert "total" in pagination, "Pagination should contain 'total'"
        
        if json_data["data"]:
            first_item = json_data["data"][0]
            for key in expected_keys:
                assert key in first_item, f"Data item should contain '{key}' field"

    @pytest.mark.parametrize("limit,offset", [
        (1, 0),
        (10, 0),
        (50, 10),
        (100, 50),
    ])
    def test_pagination_parameters(self, api_client, limit, offset):
        # TC002
        response = api_client.get_countries(limit=limit, offset=offset)
        
        assert response.status_code == 200
        
        json_data = response.json()
        pagination = json_data["pagination"]
        
        assert pagination["limit"] == limit, f"Expected limit {limit}, got {pagination['limit']}"
        assert pagination["offset"] == offset, f"Expected offset {offset}, got {pagination['offset']}"
        assert pagination["count"] <= limit, f"Count {pagination['count']} should not exceed limit {limit}"

    @pytest.mark.parametrize("endpoint_name,endpoint_path", [
        ("airports", Config.ENDPOINTS["airports"]),
        ("airlines", Config.ENDPOINTS["airlines"]),
        ("countries", Config.ENDPOINTS["countries"]),
    ])
    def test_response_contains_valid_data_count(self, api_client, endpoint_name, endpoint_path):
        # TC003
        response = api_client.get_endpoint(endpoint_path, limit=10)
        
        assert response.status_code == 200
        
        json_data = response.json()
        data_count = len(json_data["data"])
        pagination_count = json_data["pagination"]["count"]
        
        assert data_count == pagination_count, \
            f"Data array length ({data_count}) should match pagination count ({pagination_count})"

    def test_invalid_api_key_returns_error(self, api_client_invalid_key):
        # TC004
        response = api_client_invalid_key.get_countries(limit=1)

        assert response.status_code == 401
        
        json_data = response.json()
        
        assert "error" in json_data, "Response should contain 'error' object for invalid API key"
        
        error = json_data["error"]
        assert "code" in error, "Error should contain 'code' field"
        assert "message" in error, "Error should contain 'message' field"
        assert error["code"] == "invalid_access_key", \
            f"Expected 'invalid_access_key' error code, got '{error['code']}'"
        assert "valid API Access Key" in error["message"], \
            f"Error message should mention 'valid API Access Key', got '{error['message']}'"

    def test_invalid_endpoint_returns_error(self, api_client):
        # TC005
        response = api_client.get_endpoint("/invalid_endpoint_xyz", limit=1)

        assert response.status_code == 404
        
        json_data = response.json()
        
        assert "error" in json_data, "Response should contain 'error' object for invalid endpoint"
        
        error = json_data["error"]
        assert "code" in error, "Error should contain 'code' field"

    @pytest.mark.parametrize("country_field,expected_type", [
        ("country_name", str),
        ("country_iso2", str),
        ("country_iso3", str),
        ("capital", str),
        ("continent", str),
    ])
    def test_countries_data_types(self, api_client, country_field, expected_type):
        # TC006
        response = api_client.get_countries(limit=5)
        
        assert response.status_code == 200
        
        json_data = response.json()
        
        for country in json_data["data"]:
            if country.get(country_field) is not None:
                assert isinstance(country[country_field], expected_type), \
                    f"Field '{country_field}' should be of type {expected_type.__name__}"

    @pytest.mark.parametrize("airport_field", [
        "airport_name",
        "iata_code", 
        "icao_code",
        "latitude",
        "longitude",
        "country_name",
        "timezone",
    ])
    def test_airports_required_fields_present(self, api_client, airport_field):
        # TC007
        response = api_client.get_airports(limit=5)
        
        assert response.status_code == 200
        
        json_data = response.json()
        
        for airport in json_data["data"]:
            assert airport_field in airport, \
                f"Airport data should contain '{airport_field}' field"

    @pytest.mark.parametrize("airline_field,validation_func", [
        ("iata_code", lambda x: x is None or (isinstance(x, str) and len(x) <= 3)),
        ("icao_code", lambda x: x is None or (isinstance(x, str) and len(x) <= 4)),
        ("status", lambda x: x is None or x in ["active", "inactive", "unknown"]),
    ])
    def test_airlines_field_validation(self, api_client, airline_field, validation_func):
        # TC008
        response = api_client.get_airlines(limit=10)
        
        assert response.status_code == 200
        
        json_data = response.json()
        
        for airline in json_data["data"]:
            field_value = airline.get(airline_field)
            assert validation_func(field_value), \
                f"Field '{airline_field}' value '{field_value}' failed validation"

    def test_response_time_acceptable(self, api_client):
        # TC009
        response = api_client.get_countries(limit=10)
        
        assert response.elapsed.total_seconds() < 10, \
            f"Response time {response.elapsed.total_seconds()}s exceeds 10s threshold"
        
        assert response.status_code == 200

    @pytest.mark.parametrize("content_type", [
        "application/json",
    ])
    def test_response_content_type(self, api_client, content_type):
        # TC010
        response = api_client.get_countries(limit=1)
        
        assert response.status_code == 200
        assert content_type in response.headers.get("Content-Type", ""), \
            f"Expected Content-Type '{content_type}', got '{response.headers.get('Content-Type')}'"

# AviationStack API Test Framework

Automated API testing framework for [AviationStack API](https://aviationstack.com/) using Python, Pytest, and Requests library.

## Project Structure

```
SportyGroupAPITest/
├── api_client.py          # API client wrapper using requests
├── config.py              # Configuration settings
├── conftest.py            # Pytest fixtures
├── requirements.txt       # Project dependencies
├── .env.example           # Environment variables template
├── README.md              # Documentation
└── tests/
    └── test_aviation_api.py   # Test cases
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   - Create a `.env` file in the project root
   - Add your AviationStack API key:
     ```
     AVIATIONSTACK_API_KEY=your_api_key_here
     ```
   - Get your free API key at: https://aviationstack.com/signup/free

3. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

## Test Cases

| Test ID | Test Name | Description | Validation Type |
|---------|-----------|-------------|-----------------|
| TC001 | `test_endpoint_returns_expected_data_structure` | Verifies each endpoint (airports, airlines, airplanes, aircraft_types, countries) returns valid JSON with expected data structure | **Schema Validation**: Checks response contains `pagination` object, `data` array, and required fields for each endpoint |
| TC002 | `test_pagination_parameters` | Verifies pagination parameters (limit, offset) work correctly | **Parameter Validation**: Confirms limit/offset values in response match request parameters |
| TC003 | `test_response_contains_valid_data_count` | Verifies response data count matches pagination count | **Data Integrity**: Ensures data array length equals pagination count value |
| TC004 | `test_invalid_api_key_returns_error` | Verifies API returns proper error for invalid API key | **Negative Testing**: Validates error response structure and `invalid_access_key` error code |
| TC005 | `test_invalid_endpoint_returns_error` | Verifies API returns proper error for invalid endpoint | **Negative Testing**: Validates error handling for non-existent endpoints |
| TC006 | `test_countries_data_types` | Verifies countries endpoint returns correct data types | **Type Validation**: Checks field values match expected Python types (str) |
| TC007 | `test_airports_required_fields_present` | Verifies airports endpoint contains all required fields | **Field Presence Validation**: Ensures essential airport fields exist in response |
| TC008 | `test_airlines_field_validation` | Verifies airlines endpoint field values meet constraints | **Business Rule Validation**: IATA codes ≤3 chars, ICAO codes ≤4 chars, valid status values |
| TC009 | `test_response_time_acceptable` | Verifies API response time is within acceptable limits | **Performance Validation**: Response time under 10 seconds threshold |
| TC010 | `test_response_content_type` | Verifies API returns correct content type header | **Header Validation**: Content-Type is `application/json` |

## Validation Types Used

### 1. Schema Validation
Validates the structure of API responses matches expected format:
- Presence of required top-level objects (`pagination`, `data`)
- Presence of required fields within data objects
- **Why**: Ensures API contract is maintained and responses are parseable

### 2. Parameter Validation
Validates that request parameters are correctly processed:
- Pagination parameters (limit, offset) are respected
- **Why**: Ensures API correctly handles client-specified parameters

### 3. Data Integrity Validation
Validates consistency between different parts of the response:
- Data array count matches pagination count
- **Why**: Ensures response metadata accurately reflects actual data

### 4. Negative Testing
Validates proper error handling:
- Invalid API key returns appropriate error
- Invalid endpoints return appropriate error
- **Why**: Ensures API fails gracefully with informative error messages

### 5. Type Validation
Validates data types of response fields:
- String fields contain strings
- **Why**: Ensures data can be correctly processed by client applications

### 6. Business Rule Validation
Validates field values meet domain-specific constraints:
- IATA codes are 2-3 characters
- ICAO codes are 3-4 characters
- Status values are from expected set
- **Why**: Ensures data quality and adherence to aviation industry standards

### 7. Performance Validation
Validates response time is acceptable:
- Response time under threshold
- **Why**: Ensures API meets performance SLAs

### 8. Header Validation
Validates HTTP response headers:
- Content-Type header is correct
- **Why**: Ensures proper content negotiation and client compatibility

## Pytest Parametrize Usage

The test suite extensively uses `@pytest.mark.parametrize` to:
- **Reduce code duplication**: Single test function covers multiple endpoints/scenarios
- **Maintain high coverage**: Each parameter combination is a separate test case
- **Improve readability**: Test data is clearly separated from test logic

Example:
```python
@pytest.mark.parametrize("endpoint,expected_keys", [
    (Config.ENDPOINTS["airports"], ["airport_name", "iata_code"]),
    (Config.ENDPOINTS["airlines"], ["airline_name", "iata_code"]),
])
def test_endpoint_returns_expected_data_structure(self, api_client, endpoint, expected_keys):
    # Single test logic, multiple test cases
```

## API Endpoints Tested

| Endpoint | Description |
|----------|-------------|
| `/airports` | Global airports data |
| `/airlines` | Airlines information |
| `/airplanes` | Aircraft/airplane data |
| `/aircraft_types` | Aircraft type classifications |
| `/countries` | Country information |
| `/flights` | Real-time flight data |

## Running Specific Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/test_aviation_api.py::TestAviationStackAPI -v

# Run specific test
pytest tests/test_aviation_api.py::TestAviationStackAPI::test_pagination_parameters -v

# Run with detailed output
pytest tests/ -v --tb=long
```

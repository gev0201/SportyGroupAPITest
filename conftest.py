import pytest
from api_client import AviationStackClient


@pytest.fixture(scope="session")
def api_client():
    return AviationStackClient()


@pytest.fixture(scope="session")
def api_client_invalid_key():
    return AviationStackClient(api_key="invalid_api_key_12345")

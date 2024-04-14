import pytest
import httpx
from fastapi.testclient import TestClient
from app.constants import TEST_API_KEY
from app.main import app


def pytest_addoption(parser):
    """CLI options"""
    parser.addoption("--testenv", action="store", default="testClient")


@pytest.fixture(scope="class")
def client(request):
    """
    Choose env - dev or prod.
    Default is testClient which performs the tests without running a server.
    """
    test_env = request.config.getoption("--testenv")
    if test_env == "testClient":
        return TestClient(app)
    elif test_env == "prod":
        return httpx.Client(base_url='') # add prod env url in the future TODO...
    elif test_env == "dev":
        return httpx.Client(base_url='http://127.0.0.1:8000')
    else:
        raise ValueError("Invalid test environment")


@pytest.fixture(scope="class")
def setup_teardown(client: TestClient | httpx.Client):
    """
    Setup and Teardown
    """
    # setup

    yield

    # teardown
    
    client.delete("/clean-test", headers={ "X-API-KEY": TEST_API_KEY })
    

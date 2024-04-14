import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app


def pytest_addoption(parser):
    parser.addoption("--testenv", action="store", default="testClient")

@pytest.fixture
def client(request):
    test_env = request.config.getoption("--testenv")
    if test_env == "testClient":
        return TestClient(app)
    elif test_env == "prod":
        return httpx.Client(base_url='') # add prod env url in the future TODO...
    elif test_env == "dev":
        return httpx.Client(base_url='http://127.0.0.1:8000')
    else:
        raise ValueError("Invalid test environment")
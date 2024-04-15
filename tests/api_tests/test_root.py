from fastapi.testclient import TestClient
from httpx import Client
from tests.api_tests.ParentAPITest import ParentAPITest

class TestRoot(ParentAPITest):
    endpointURL = "/"
    
    def test_read_root(self, client: TestClient | Client):
        response = client.get(self.endpointURL)
        expectedStatus = 200
        expectedResponse = { "API": "ON" }

        assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}, Actual status: {response.status_code}"
        assert response.json() == expectedResponse, f"Expected response: {expectedResponse}, Actual response: {response.json()}"

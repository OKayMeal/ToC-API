from httpx import Client
from fastapi.testclient import TestClient
from app.main import app


class ParentAPITest:
    """
    Parent base class for all API tests.
    It contains all things that are universal for all of the API tests
    """
    def execute_HTTP_request(self, client: TestClient | Client, method: str, url: str, headers = None, json = None, params=None, data=None, timeout=10, auth=None):
        """
        This is a http request wrapper for TestClient and httpx.Client request methods
        It unifies the usage so that no matter if the client is TestClient or httpx.Client
        the tests can be executed properly.
        """
        if type(client) is TestClient:
            with TestClient(app) as client:
                return self.HTTP_request(client=client, method=method, url=url, headers=headers, json=json, params=params, data=data, timeout=timeout, auth=auth)
        else:
            return self.HTTP_request(client=client, method=method, url=url, headers=headers, json=json, params=params, data=data, timeout=timeout, auth=auth)
        

    def HTTP_request(self, client: TestClient | Client, method: str, url: str, headers = None, json = None, params=None, data=None, timeout=10, auth=None):
        if method == "GET" or method == "get":
            return client.get(url, headers=headers, params=params, timeout=timeout, auth=auth)
        elif method == "POST" or method == "post":
            return client.post(url, headers=headers, json=json, params=params, data=data, timeout=timeout, auth=auth)
        elif method == "DELETE" or method == "delete":
            return client.delete(url, headers=headers, params=params, timeout=timeout, auth=auth)
        elif method == "PUT" or method == "put":
            return client.put(url, headers=headers, json=json, params=params, data=data, timeout=timeout, auth=auth)
        elif method == "PATCH" or method == "patch":
            return client.patch(url, headers=headers, json=json, params=params, data=data, timeout=timeout, auth=auth)
        elif method == "HEAD" or method == "head":
            return client.head(url, headers=headers, params=params, timeout=timeout, auth=auth)
        elif method == "OPTIONS" or method == "options":
            return client.options(url, headers=headers, params=params, timeout=timeout, auth=auth)
        else:
            raise ValueError("Invalid HTTP request method")
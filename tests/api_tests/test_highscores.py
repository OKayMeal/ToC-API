import copy
from datetime import datetime
from fastapi.testclient import TestClient
from httpx import Client
from app.main import app
from tests.api_tests.ParentAPITest import ParentAPITest
from app.constants import HIGHSCORE_VALID_LIST_VALUES, HIGHSCORE_VALID_NUMBERS_BOUNDARIES, TEST_API_KEY

class TestHighscores(ParentAPITest):
    endpointURL = "/highscores"
    # default valid post req body
    defaultPostReqBody = {
        "name": "tester",
        "time": "20:00:00",
        "hp": 200,
        "attack": 10,
        "defense": 5,
        "speed": 200,
        "equipment": ["FireSword", "BootsOfHaste"],
        "level": 6,
        "ng": False,
        "traps": 10,
        "keys": 12,
        "gold": 65,
        "enemies_killed": 40,
        "gold_looted": 150,
        "bosses_defeated": ["ancientScarab"]
    }
    requiredFields = list(defaultPostReqBody.keys()) # all fields are required
    validFieldValues = HIGHSCORE_VALID_LIST_VALUES # valid fields' values for equipment and bosses_defeated
    validNumbersBoundaries = HIGHSCORE_VALID_NUMBERS_BOUNDARIES # valid boundaries in format { {"field1": "min": 1, "max": 5}, ... }
    invalidAPIKey = { "X-API-KEY": "invalidkey-123-123-123" }
    validAPIKey = { "X-API-KEY": TEST_API_KEY }
    todayDate = datetime.now().strftime('%Y-%m-%d')

    # NEGATIVE TESTS #

    # authorization
    def test_get_no_api_key(self, client: TestClient | Client):
        expectedStatus = 401
        expectedMessage = { "detail": "API key missing" }

        response = self.execute_HTTP_request(client=client, method="GET", url=self.endpointURL)
        assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code}"
        assert response.json() == expectedMessage, f"Expected message: {expectedMessage}. Actual message: {response.json()}"


    def test_post_no_api_key(self, client: TestClient | Client):
        expectedStatus = 401
        expectedMessage = { "detail": "API key missing" }

        response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, json=self.defaultPostReqBody)
        assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code}"
        assert response.json() == expectedMessage, f"Expected message: {expectedMessage}. Actual message: {response.json()}"
    
    
    def test_get_invalid_api_key(self, client: TestClient | Client):
        expectedStatus = 401
        expectedMessage = { "detail": "Invalid API key" }

        response = self.execute_HTTP_request(client=client, method="GET", url=self.endpointURL, headers=self.invalidAPIKey)
        assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code}"
        assert response.json() == expectedMessage, f"Expected message: {expectedMessage}. Actual message: {response.json()}"
    

    def test_post_invalid_api_key(self, client: TestClient | Client):
        expectedStatus = 401
        expectedMessage = { "detail": "Invalid API key" }

        response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, headers=self.invalidAPIKey, json=self.defaultPostReqBody)
        assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code}"
        assert response.json() == expectedMessage, f"Expected message: {expectedMessage}. Actual message: {response.json()}"
    

    # required fields
    def test_post_missing_required_fields(self, client: TestClient | Client):
        expectedStatus = 422
        expectedMessage = "Field required"

        for requiredField in self.requiredFields:
            # get default valid post req body
            reqBody = copy.deepcopy(self.defaultPostReqBody)
            # delete reqd field
            del reqBody[requiredField]

            response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, headers=self.validAPIKey, json=reqBody)
            assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code} for field: {requiredField}"

            responseData = response.json()
            # check if 'detail' key exists and it contains at least one item
            assert "detail" in responseData and len(responseData["detail"]) > 0, f"Response JSON does not contain 'detail' key or it's empty for field: {requiredField}"

            errorMessage = responseData["detail"][0].get("msg", "")
            assert errorMessage == expectedMessage, f"Expected message: {expectedMessage}. Actual message: {errorMessage} for field: {requiredField} Input: {reqBody}"
    

    # data types
    def test_post_invalid_data_types(self, client: TestClient | Client):
        expectedStatus = 422
        expectedMessage = "Input should be" # a valid integer, a valid boolean etc.

        reqBodyInvalidDataTypes = {
            "name": 123,
            "time": 20,
            "hp": "a lot of hp",
            "attack": "strongAttack",
            "defense": ['defense', 'defense'],
            "speed": "superSonicSpeed",
            "equipment": [2, 15],
            "level": "highLevel",
            "ng": 5,
            "traps": ["this", "is", "a", "trap"],
            "keys": [1, 2, 6],
            "gold": [],
            "enemies_killed": "everybody",
            "gold_looted": " a lot",
            "bosses_defeated": [1, 2]
        }

        for requiredField in self.requiredFields:
            # get default valid post req body
            reqBody = copy.deepcopy(self.defaultPostReqBody)
            # change the reqd field value to incorrect data type example
            reqBody[requiredField] = reqBodyInvalidDataTypes[requiredField]

            response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, headers=self.validAPIKey, json=reqBody)
            assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code} for field: {requiredField}"

            responseData = response.json()
            # check if 'detail' key exists and it contains at least one item
            assert "detail" in responseData and len(responseData["detail"]) > 0, f"Response JSON does not contain 'detail' key or it's empty for field: {requiredField}"

            errorMessage = responseData["detail"][0].get("msg", "")
            assert expectedMessage in errorMessage, f"Expected message: {expectedMessage}. Actual message: {errorMessage} for field: {requiredField} Input: {reqBody}"


    # data
    def test_post_invalid_data_equipment_bosses_defeated(self, client: TestClient | Client):
        """
        Test for invalid values for fields 'equipment' and 'bosses_defeated'
        """
        expectedStatus = 422
        expectedMessage = "Value error"

        testedFields = ['equipment', 'bosses_defeated']
        invalidData = [["superCoolItemThatDoesNotExist", "FireSword"], ["theStrongestBossInTheUniverse"]]
        
        for index, field in enumerate(testedFields):
            # get default valid post req body
            reqBody = copy.deepcopy(self.defaultPostReqBody)
            # change field value to non-existent eq/boss
            reqBody[field] = invalidData[index]

            response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, headers=self.validAPIKey, json=reqBody)
            assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code} for field: {field}"

            responseData = response.json()
            # check if 'detail' key exists and it contains at least one item
            assert "detail" in responseData and len(responseData["detail"]) > 0, f"Response JSON does not contain 'detail' key or it's empty for field: {field}"

            errorMessage = responseData["detail"][0].get("msg", "")
            assert expectedMessage in errorMessage, f"Expected message: {expectedMessage}. Actual message: {errorMessage} for field: {field}. Input: {reqBody}"
    

    def test_post_invalid_data_numbers(self, client: TestClient | Client):
        """
        Test for invalid values for all fields that expect an int in a certain range
        """
        expectedStatus = 422
        expectedMessage = "Value error"
        
        for field in self.validNumbersBoundaries:
            for case in self.validNumbersBoundaries[field]:
                inputVal = self.validNumbersBoundaries[field][case]
                if case == 'min':
                    inputVal -= 1 # check value outside of the boundary
                elif case == 'max':
                    inputVal += 1 # check value outside of the boundary
                
                reqBody = copy.deepcopy(self.defaultPostReqBody)
                reqBody[field] = inputVal
                
                response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, headers=self.validAPIKey, json=reqBody)
                assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code} for field: {field}"

                responseData = response.json()
                # check if 'detail' key exists and it contains at least one item
                assert "detail" in responseData and len(responseData["detail"]) > 0, f"Response JSON does not contain 'detail' key or it's empty for field: {field}"

                errorMessage = responseData["detail"][0].get("msg", "")
                assert expectedMessage in errorMessage, f"Expected message: {expectedMessage}. Actual message: {errorMessage} for field: {field} Input: {inputVal}"


    def test_post_invalid_data_name(self, client: TestClient | Client):
        expectedStatus = 422
        expectedMessage = "Value error"

        testValues = ["", "NameThatIsLongerThan30Character"] # 31 chars

        for value in testValues:
            reqBody = copy.deepcopy(self.defaultPostReqBody)
            reqBody["name"] = value
                
            response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, headers=self.validAPIKey, json=reqBody)
            assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code} for field name"

            responseData = response.json()
            # check if 'detail' key exists and it contains at least one item
            assert "detail" in responseData and len(responseData["detail"]) > 0, f"Response JSON does not contain 'detail' key or it's empty for field: name"

            errorMessage = responseData["detail"][0].get("msg", "")
            assert expectedMessage in errorMessage, f"Expected message: {expectedMessage}. Actual message: {errorMessage} for field: name Input: {value}"


    # POSITIVE TESTS # 
    def test_scenario_post_get(self, client: TestClient | Client, setup_teardown):
        """
        Test POSTing a highscore and then GETting highscore
        """
        expectedStatus = 201
        expectedMessage = "created successfully"

        # 1. Post highscores
        response = self.execute_HTTP_request(client=client, method="POST", url=self.endpointURL, headers=self.validAPIKey, json=self.defaultPostReqBody)
        assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code} for POST highscore"
        
        responseData = response.json()
        # check if 'msg' key exists and it contains at least one item
        assert "msg" in responseData and len(responseData["msg"]) > 0, f"Response JSON does not contain 'msg' key or it's empty for POST highscore"

        responseMessage = responseData.get("msg", "")
        assert expectedMessage in responseMessage, f"Expected message: {expectedMessage}. Actual message: {responseMessage} for POST highscore"

        # check if the response contains newly created highscore record
        assert "highscore" in responseData and len(responseData["highscore"]) > 0, f"Response JSON does not contain 'highscore' key or it's empty for POST highscore"

        # check if the today date has been added to the record
        assert "date" in responseData["highscore"] and len(responseData["highscore"]["date"]) > 0, f"Response JSON does not contain 'date' key or it's empty for POST highscore"
        assert self.todayDate in responseData["highscore"]["date"], f"The date in created record is not a current date. Today date: {self.todayDate}. Record date: {responseData['highscore']['date']}"

        # check if UUID has been added to the record
        assert "uuid" in responseData["highscore"] and len(responseData["highscore"]["uuid"]) > 0, f"Response JSON does not contain 'uuid' key or it's empty for POST highscore"
        
        # save the uuid
        recordUUID = responseData["highscore"]["uuid"]

        # 2. GET highscores
        expectedStatus = 200
        
        response = self.execute_HTTP_request(client=client, method="GET", url=self.endpointURL, headers=self.validAPIKey)
        assert response.status_code == expectedStatus, f"Expected status: {expectedStatus}. Actual status: {response.status_code} for GET highscore"

        responseData = response.json()
        # check if responseData is a list
        assert isinstance(responseData, list), f"Expected type of response data is 'list'. Actual type: {type(responseData)}"

        recordFound = False
        for record in responseData:
            # check if a record in responseData is a dict
            assert isinstance(record, dict), f"Expected type of elements in response data is 'dict'. Actual type: {type(record)}"

            # check if a record matches UUID
            if record["uuid"] == recordUUID:
                recordFound = True

        assert recordFound, f"Record created in POST highscores with UUID '{recordUUID}' not found in GET highscores responseData: {responseData}"





API and automated API tests for the Tombs of Cherem web game

The Tombs of Cherem game - https://tombs-of-cherem.vercel.app/

HOW TO INSTALL AND RUN API:
  1. Clone the repo
  2. Install all dependencies from requirements.txt - "pip install -r requirements.txt"
  3. Go to root dir ./
  5. In terminal type "uvicorn app.main:app --reload"
  6. API runs locally on http://127.0.0.1:8000 by default

HOW TO RUN API TESTS:
There are 3 possible ways to run API tests:
  1. Using FastAPI TestClient which runs the tests locally without the need to start the API server - type **pytest -v ./tests/api_tests**
  2. On production env - **pytest -v ./tests/api_tests --testenv=prod**
  3. On dev env locally - requires starting the app first as instructed above in "HOW TO INSTALL AND RUN API" - **pytest -v ./tests/api_tests --testenv=dev**

HOW TO RUN UNIT TESTS:
  1. pytest -v ./tests/unit_tests

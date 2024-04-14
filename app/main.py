from fastapi import Depends, FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from app.constants import TEST_API_KEY
from .dependencies import Dependencies
from .routers import highscores
from .database.QueryManager import QueryManager
from .exceptions import exceptions

queryManager = QueryManager()
testQueryManager = QueryManager(test=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # RUNS ON SERVER START
    # create empty tables if they don't exist already for both prod and test db
    await queryManager.create_empty_tables()
    await testQueryManager.create_empty_tables()

    # test
    # await queryManager.execute_many_query("""
    #                             INSERT INTO keys (type, key, expires)
    #                             VALUES (:type, :key, :expires);
    #                         """, [{"type": "save", "key": "123123", "expires": "2024-02-15 12:00"}, {"type": "save", "key": "12312322", "expires": "2024-05-15 12:00"}, {"type": "save", "key": "12312223", "expires": "2024-06-15 12:00"}])
    
    # load and check the API key
    await queryManager.check_keys()

    yield
    # RUNS ON SERVER SHUTTING DOWN


    
app = FastAPI(lifespan=lifespan)
app.include_router(highscores.router)

@app.exception_handler(exceptions.DatabaseConnectionError)
async def db_connection_failed_handler(request: Request, exc: exceptions.DatabaseConnectionError):
    return JSONResponse(
        status_code=503,
        content={"message": "Service temporarily unavailable, please try again later."},
    )


@app.get("/")
def read_root():
    """Status check-up"""
    return { "API": "ON" }


@app.delete("/clean-test")
async def clean_test_db(api_key: str = Depends(Dependencies.verify_API_key)):
    """
    Cleans test database
    """
    if (api_key == TEST_API_KEY):
        await testQueryManager.execute_query(testQueryManager.deleteAllHighScores)
        
        return { "message": "All test data deleted successfully!" }
    else:
        raise HTTPException(status_code=400, detail="Test API Key required to delete test data")


# ENDPOINTS CREATED FOR DEBUGGING PURPOSES
@app.get("/keys")
async def read_keys_test():
    """
    For debugging purposes
    """
    keys = await queryManager.fetch_rows("SELECT * FROM keys")

    return keys



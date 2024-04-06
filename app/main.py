from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from .routers import highscores
from .database import QueryManager
from .exceptions import exceptions

queryManager = QueryManager.QueryManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # RUNS ON SERVER START
    # create empty tables if they don't exist already
    await queryManager.create_empty_tables()

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
    return {"API": "ON"}

# ENDPOINTS CREATED FOR DEBUGGING PURPOSES
@app.get("/keys")
async def read_keys_test():
    """
    For debugging purposes
    """
    keys = await queryManager.fetch_rows("SELECT * FROM keys")

    return keys



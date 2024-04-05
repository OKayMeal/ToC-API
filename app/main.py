from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from .routers import highscores
from .database import QueryManager
from .exceptions import exceptions

queryManager = QueryManager.QueryManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create empty highscores table if not exists
    await queryManager.execute_query(queryManager.createHighscoresTable)
    
    yield


    
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




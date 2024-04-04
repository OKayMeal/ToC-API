from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
import sqlite3
from .routers import highscores
from .database import QueryManager

queryManager = QueryManager.QueryManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # establish db connection
    connection = sqlite3.connect("../toc.db")

    # cursor obj to execute SQL
    cursor = connection.cursor()
    # create empty highscores table if not exists
    cursor.execute(queryManager.createHighscoresTable)

    # commit the changes
    connection.commit()

    # pass connection and cursor to app state
    app.state.dbConnection = connection
    app.state.dbCursor = cursor
    
    yield

    connection.close()
    

app = FastAPI(lifespan=lifespan)
app.include_router(highscores.router)


@app.get("/")
def read_root():
    return {"API": "ON"}




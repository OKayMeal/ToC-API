from typing import Union
from fastapi import APIRouter
from ..database import QueryManager

router = APIRouter()
queryManager = QueryManager.QueryManager()

@router.get("/highscores")
async def read_highscores():
    
    highscores = await queryManager.fetch_rows(queryManager.readAllHighScores)
    
    return highscores

from fastapi import APIRouter, Request
from ..database import QueryManager

router = APIRouter()
queryManager = QueryManager.QueryManager()

@router.get("/highscores")
async def read_highscores(request: Request):
    response = request.app.state.dbCursor.execute(queryManager.readAllHighScores)
    
    return response

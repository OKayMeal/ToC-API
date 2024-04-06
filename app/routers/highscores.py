from fastapi import APIRouter, Depends
from ..dependencies import Dependencies
from ..database import QueryManager
from ..models.HighScore import HighScore

router = APIRouter()
queryManager = QueryManager.QueryManager()

@router.get("/highscores")
async def read_highscores():
    
    highscores = await queryManager.fetch_rows(queryManager.readAllHighScores)
    
    return highscores


@router.post("/highscores")
async def post_highscores(highscore: HighScore, api_key: str = Depends(Dependencies.verify_API_key)):
    
    return highscore

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.constants import TEST_API_KEY
from ..dependencies import Dependencies
from ..database.QueryManager import QueryManager
from ..models.HighScore import HighScore

router = APIRouter()

@router.get("/highscores")
async def read_highscores(api_key: str = Depends(Dependencies.verify_API_key)):
    queryManager = QueryManager(test=(api_key == TEST_API_KEY))
    highscores = await queryManager.fetch_rows(queryManager.readAllHighScores)

    # reconvert from SQLite data format
    highscores = HighScore.revert_clean_data(highscores, ['ng'], ['equipment', 'bosses_defeated'])
    
    return highscores


@router.post("/highscores", status_code=status.HTTP_201_CREATED)
async def post_highscores(highscore: HighScore, api_key: str = Depends(Dependencies.verify_API_key)):
    queryManager = QueryManager(test=(api_key == TEST_API_KEY))
    modelDict = highscore.clean_data(highscore.model_dump())
    
    try:
        await queryManager.execute_query(queryManager.postHighScore, modelDict)
    except:
        raise HTTPException(status_code=400, detail="Invalid data")
    
    return JSONResponse(
        status_code=201,
        content={ "msg": "Highscore created successfully", "highscore": modelDict },
    )

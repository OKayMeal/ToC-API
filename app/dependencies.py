from typing import Annotated
from fastapi import Header, HTTPException
from app.constants import TEST_API_KEY
from .database.QueryManager import QueryManager

queryManager = QueryManager()

class Dependencies:
    
    @classmethod
    async def verify_API_key(cls, x_api_key: Annotated[str | None, Header()] = None):
        """
        Verifies the API key in the request header
        """
        if not x_api_key:
            raise HTTPException(status_code=401, detail="API key missing")
        
        # check if it's a test key first
        if x_api_key != TEST_API_KEY:
            allKeys = await queryManager.fetch_rows(queryManager.readAllKeysType, { "type": "save" })

            if len(allKeys) > 0:
                if x_api_key != allKeys[0]["key"]:
                    raise HTTPException(status_code=401, detail="Invalid API key")
        
        return x_api_key
        


from typing import Annotated
from fastapi import Header, HTTPException
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
        
        allKeys = await queryManager.fetch_rows(queryManager.readAllKeysType, { "type": "save" })

        if len(allKeys) > 0:
            if x_api_key != allKeys[0]["key"]:
                raise HTTPException(status_code=400, detail="Invalid API key")
        


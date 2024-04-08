import json
from datetime import datetime
from databases import Database
from ..exceptions import exceptions

class QueryManager:
    DATABASE_URL = "sqlite+aiosqlite:///./toc.db"
    KEY_URL = "./key.json"
    db = Database(DATABASE_URL)

    # CREATE TABLES QUERIES
    createHighscoresTable = """
                                CREATE TABLE IF NOT EXISTS highscores 
                                (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    uuid TEXT NOT NULL,
                                    name TEXT NOT NULL,
                                    date TEXT NOT NULL,
                                    time TEXT NOT NULL,
                                    hp INTEGER NOT NULL,
                                    attack INTEGER NOT NULL,
                                    defense INTEGER NOT NULL,
                                    speed INTEGER NOT NULL,
                                    equipment TEXT NOT NULL,
                                    level INTEGER NOT NULL,
                                    ng INTEGER NOT NULL,
                                    traps INTEGER NOT NULL,
                                    keys INTEGER NOT NULL,
                                    gold INTEGER NOT NULL,
                                    enemies_killed INTEGER NOT NULL,
                                    gold_looted INTEGER NOT NULL,
                                    bosses_defeated TEXT NOT NULL
                                );
                            """
    createKeysTable =       """
                                CREATE TABLE IF NOT EXISTS keys 
                                (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    type TEXT NOT NULL,
                                    key TEXT NOT NULL,
                                    expires TEXT NOT NULL
                                );
                            """
    # READ ROWS QUERIES
    readAllKeysType =       """
                                SELECT * FROM keys WHERE type = :type;
                            """
    readAllHighScores =     """
                                SELECT * FROM highscores;
                            """
    # POST ROWS QUERIES
    postKey =               """
                                INSERT INTO keys (type, key, expires)
                                VALUES (:type, :key, :expires);
                            """
    postHighScore =         """
                                INSERT INTO highscores (
                                    uuid, name, date, time, hp, attack, defense,
                                    speed, equipment, level, ng, traps,
                                    keys, gold, enemies_killed, gold_looted,
                                    bosses_defeated
                                )
                                VALUES (
                                    :uuid, :name, :date, :time, :hp, :attack, :defense,
                                    :speed, :equipment, :level, :ng, :traps,
                                    :keys, :gold, :enemies_killed, :gold_looted,
                                    :bosses_defeated
                                );
                            """
    # DELETE ROWS QUERIES
    deleteKeyType =         """
                                DELETE FROM keys WHERE type = :type;
                            """
    deleteKeyByID =         """
                                DELETE FROM keys WHERE id = :id;
                            """


    async def check_keys(self):
        """
        Handles the process of checking the API key on the server start.
        First it attempts to load the fresh key from .json and compares it with DB.
        Provided the .json key is up-to-date, it cleans the DB from old keys and puts there the .json one
        """
        # fetch all keys of type "save" from DB
        allSaveKeys = await self.fetch_rows(self.readAllKeysType, { "type": "save" })
        dbEmpty = False

        if len(allSaveKeys) == 0:
            dbEmpty = True


        try:
            # try to load key.json file
            data = self.load_key(self.KEY_URL)
            print(data)

        except (exceptions.FileNotFoundError, exceptions.WrongFileFormat) as e:
            print(f"Exception: {e}")

            if dbEmpty:
                raise Exception("API key of type 'save' not found in DB")
            
            else:
                # compare dates and clear older and if only one and not expired just leave it

                if len(allSaveKeys) == 1:
                    if self.is_expired(allSaveKeys[0]["expires"]):
                        # the only key in DB is expired and no .json so raise error
                        raise exceptions.KeyExpired("The key found in DB is expired")
                    else:
                        # do nothing, keep the non-expired key in DB - assume it's the up-to-date one to use
                        print("The key found in DB is NOT expired. Please remember to add UPDATED ./key.json file!")
                        return
                else:
                    # there are more than one key in DB
                    keysToDelete: list[dict[str, int]] = []
                    keysNotExpired: list[dict] = []

                    # iterate over the keys and seperate expired from non-expired
                    for key in allSaveKeys:
                        id = { "id": key["id"] }
                        date = { "expires": key["expires"] }
                        expiresDate = date["expires"]

                        if self.is_expired(expiresDate):
                            keysToDelete.append(id)
                        else:
                            keysNotExpired.append({ **id, **date })
                    
                    if len(keysToDelete) == len(allSaveKeys):
                        # means all of the keys in DB are expired so it's high time to delete them
                        print("All of the keys found in DB are expired.")
                        print("Deleting the expired keys...")
                        await self.execute_many_query(self.deleteKeyByID, keysToDelete)
                        raise Exception("All of the keys found in DB are expired.")
                    
                    else:
                        # means there are some keys that aren't expired - find the most recent
                        today = datetime.now()
                        minDeltaTime = -1
                        for key in keysNotExpired:
                            # calc delta time
                            deltaTime = today - datetime.strptime(key["expires"], "%Y-%m-%d %H:%M")
                            deltaTimeInt = int(deltaTime.total_seconds())
                            key["deltaTime"] = deltaTimeInt

                            # check if it's the most recent
                            minDeltaTime = min(minDeltaTime, key["deltaTime"])
                          
                        
                        for key in keysNotExpired:
                            # check for all older than the most recent and delete them
                            if key["deltaTime"] != minDeltaTime:
                                keysToDelete.append({ "id": key["id"] })
                        
                        print("Not expired key has been found in db. However, please update your key.json file!")
                        return await self.execute_many_query(self.deleteKeyByID, keysToDelete)
                        


        if not dbEmpty:
            # delete all keys of type "save"
            print("Deleting all old keys of type 'save'")
            await self.execute_query(self.deleteKeyType, { "type": "save" })

        # check if .json key not expired
        if not self.is_expired(data["expires"]):
            return await self.execute_query(self.postKey, { "type": data["type"], "key": data["key"], "expires": data["expires"] })
        else:
            raise Exception("Key from .json expired")
         


    def load_key(self, file_path: str):
        """
        Loads the API key from .json file
        """
        try:
            with open(file_path, 'r') as file:
                # parse the JSON data to dict
                data: dict[str, str] = json.load(file)

                if not isinstance(data, dict):
                    raise exceptions.WrongFileFormat("The data loaded is not of dict type")
                
                if "type" not in data or "key" not in data or "expires" not in data:
                    raise exceptions.WrongFileFormat("The data loaded has wrong format - missing keys")


        except Exception as e:
            raise exceptions.FileNotFoundError("Failed to load key.json file") from e

        return data


    def is_expired(self, dateStr: str):
        """
        Checks if the date is expired
        """
        today = datetime.now()
        date = datetime.strptime(dateStr, "%Y-%m-%d %H:%M")

        return today > date
    

    async def create_empty_tables(self):
        """
        Creates all required empty tables if they don't exist already
        """
        await self.execute_query(self.createHighscoresTable)
        await self.execute_query(self.createKeysTable)


    async def execute_query(self, query: str, values: dict | None = None):
        """
        Executes the query
        """
        await self.connect_db()

        await self.db.execute(query=query, values=values)        


    async def execute_many_query(self, query: str, values: dict | None = None):
        """
        Executes the query * sets of values
        For example values = [
                                {"text": "example2", "completed": False},
                                {"text": "example3", "completed": True},
                            ]
        The query would be executed twice since there are two sets of values
        """
        await self.connect_db()

        await self.db.execute_many(query=query, values=values)


    async def fetch_rows(self, query: str, values: dict | None = None):
        """
        Fetches all rows as per query and values
        """
        await self.connect_db()

        return await self.db.fetch_all(query=query, values=values)


    async def connect_db(self):
        """
        Connects to SQLite db
        """
        try:
            await self.db.connect()
        except Exception as e:
            raise exceptions.DatabaseConnectionError("Failed to connect to the database") from e

        

    
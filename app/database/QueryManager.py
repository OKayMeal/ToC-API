import json
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
    # DELETE ROWS QUERIES
    deleteKeyType =         """
                                DELETE FROM keys WHERE type = :type;
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
                pass
        

        if dbEmpty:
            # key in .json, but not in DB -> post a fresh key to DB
            return await self.execute_query(self.postKey, { "type": data["type"], "key": data["key"], "expires": data["expires"] })
        
        else:
            # compare dates with the .json one and if .json is fresh, clear all and post .json or if one of db's is fresh then clear rest
            pass




    def compare_expiry_dates(self):
        pass

    
    def load_key(self, file_path: str):
        """
        Loads the API key from .json file
        """
        try:
            with open(file_path, 'r') as file:
                # parse the JSON data to dict
                data: dict[str, str] = json.load(file)

                if not isinstance(data, dict[str, str]):
                    raise exceptions.WrongFileFormat("The data loaded is not of dict[str, str] type")
                
                if "type" not in data or "key" not in data or "expires" not in data:
                    raise exceptions.WrongFileFormat("The data loaded has wrong format - missing keys")


        except Exception as e:
            raise exceptions.FileNotFoundError("Failed to load key.json file") from e

        return data


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

        

    
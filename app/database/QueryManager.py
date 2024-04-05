from databases import Database
from ..exceptions import exceptions

class QueryManager:
    DATABASE_URL = "sqlite+aiosqlite:///./toc.db"
    db = Database(DATABASE_URL)
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
    readAllHighScores = """
                            SELECT * FROM highscores;
                        """


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

        

    
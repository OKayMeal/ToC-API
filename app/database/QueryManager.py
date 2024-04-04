class QueryManager:
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

    def __init__(self):
        pass

    
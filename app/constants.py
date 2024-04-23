from app.RootDirFinder import RootDirFinder
rootDirFinder = RootDirFinder()


# URLs and keys #
DATABASE_URL = f"sqlite+aiosqlite:///{rootDirFinder.find_project_root(rootDirFinder.currentFilePath)}/toc.db"
DATABASE_FILE_PATH = f"{rootDirFinder.find_project_root(rootDirFinder.currentFilePath)}/toc.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{rootDirFinder.find_project_root(rootDirFinder.currentFilePath)}/test_toc.db"
TEST_API_KEY = "5ce7bda6-74e8-4a0f-9616-b14b9ca5f3b1"
KEY_URL = f"{rootDirFinder.find_project_root(rootDirFinder.currentFilePath)}/key.json"


# MODELS VALID VALUES #

# Highscore
HIGHSCORE_VALID_NUMBERS_BOUNDARIES = {
    "hp": {
        "min": 150,
        "max": 999
    },
    "attack": {
        "min": 5,
        "max": 99
    },
    "defense": {
        "min": 5,
        "max": 99
    },
    "speed": {
        "min": 100,
        "max": 999
    },
    "level": {
        "min": 1,
        "max": 8
    },
    "traps": {
        "min": 0,
        "max": 999
    },
    "keys": {
        "min": 0,
        "max": 999
    },
    "gold": {
        "min": 0,
        "max": 999
    },
    "enemies_killed": {
        "min": 0,
        "max": 999
    },
    "gold_looted": {
        "min": 0,
        "max": 999
    },
}

HIGHSCORE_VALID_LIST_VALUES = {
    "equipment": [
        'BootsOfHaste', 'NobleArmor', 'FireSword', 'ScarabShield', 'WandOfInferno',
        'SkullStaff', 'ankhGolden', 'ankhSilver',
    ],
    "bosses_defeated": [
        'pharaoh', 'ancientScarab',
    ],
}
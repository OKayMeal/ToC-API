from pydantic import BaseModel, validator

class HighScore(BaseModel):
    name: str
    date: str | None = None
    time: str
    hp: int
    attack: int
    defense: int
    speed: int
    equipment: list[str]
    level: int
    ng: bool
    traps: int
    keys: int
    gold: int
    enemies_killed: int
    gold_looted: int
    bosses_defeated: list[str]

    @validator('name')
    def name_validator(cls, name):
        if len(name) > 30:
            raise ValueError('Name cannot be longer than 30 characters')
        if len(name) == 0:
            raise ValueError('Name cannot be empty')
        
        return name
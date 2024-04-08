from pydantic import field_validator
from typing import ClassVar
from .ParentModel import ParentModel

class HighScore(ParentModel):
    # REQUEST BODY FIELDS #
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

    # VALID VALUES FOR VALIDATION PURPOSES #
    numbersBoundaries: ClassVar[dict[str, dict[str, int]]] = {
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
    validListValues: ClassVar[dict[str, list[str]]] = {
        "equipment": [
            'BootsOfHaste', 'NobleArmor', 'FireSword', 'ScarabShield', 'WandOfInferno',
            'SkullStaff', 'ankhGolden', 'ankhSilver',
        ],
        "bosses_defeated": [
            'pharaoh', 'ancientScarab',
        ],
    }


    # FIELD VALIDATORS #
    @field_validator('name')
    def name_validator(cls, name: str):
        return cls.validate_string_length("name", name, 30, True)
    

    @field_validator('time')
    def time_validator(cls, time: str):
        return cls.validate_time(time)
    

    @field_validator('hp')
    def hp_validator(cls, hp: int):
        return cls.validate_numbers_boundaries("hp", hp)
    

    @field_validator('attack')
    def attack_validator(cls, attack: int):
        return cls.validate_numbers_boundaries("attack", attack)
    

    @field_validator('defense')
    def defense_validator(cls, defense: int):
        return cls.validate_numbers_boundaries("defense", defense)
    

    @field_validator('speed')
    def speed_validator(cls, speed: int):
        return cls.validate_numbers_boundaries("speed", speed)
    

    @field_validator('equipment')
    def equipment_validator(cls, equipment: list[str]):
        return cls.validate_list_values("equipment", equipment)
    

    @field_validator('level')
    def level_validator(cls, level: int):
        return cls.validate_numbers_boundaries("level", level)
    

    @field_validator('traps')
    def traps_validator(cls, traps: int):
        return cls.validate_numbers_boundaries("traps", traps)
    

    @field_validator('keys')
    def keys_validator(cls, keys: int):
        return cls.validate_numbers_boundaries("keys", keys)
    

    @field_validator('gold')
    def gold_validator(cls, gold: int):
        return cls.validate_numbers_boundaries("gold", gold)
    

    @field_validator('enemies_killed')
    def enemies_killed_validator(cls, enemies_killed: int):
        return cls.validate_numbers_boundaries("enemies_killed", enemies_killed)
    

    @field_validator('gold_looted')
    def gold_looted_validator(cls, gold_looted: int):
        return cls.validate_numbers_boundaries("gold_looted", gold_looted)
    

    @field_validator('bosses_defeated')
    def bosses_defeated_validator(cls, bosses_defeated: list[str]):
        return cls.validate_list_values("bosses_defeated", bosses_defeated)
    
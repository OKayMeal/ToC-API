from pydantic import BaseModel, field_validator
from typing import ClassVar
import re

class HighScore(BaseModel):
    # REQUEST BODY FIELDS #
    name: str
    date: str | None = None # handle this bad boy TODO...
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
        if len(name) > 30:
            raise ValueError('Name cannot be longer than 30 characters')
        if len(name) == 0:
            raise ValueError('Name cannot be empty')
        
        return name
    

    @field_validator('time')
    def time_validator(cls, time: str):
        # check the time format using regex
        if not re.match(r'^\d{2}:\d{2}:\d{2}$', time):
            raise ValueError('Time must be in HH:MM:SS format')
        
        # split the string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, time.split(':'))

        # Validate hours, minutes, and seconds
        if not (0 <= hours <= 23):
            raise ValueError('Hours must be between 00 and 23')
        if not (0 <= minutes <= 59):
            raise ValueError('Minutes must be between 00 and 59')
        if not (0 <= seconds <= 59):
            raise ValueError('Seconds must be between 00 and 59')

        return time
    

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
        # TODO...
        # for example check if it consists real game items
        return equipment
    

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
    

    @field_validator('defense')
    def bosses_defeated_validator(cls, bosses_defeated: list[str]):
        # TODO...
        # check if the values in a list actually exist in game
        return bosses_defeated
    


    # GENERIC VALIDATING METHODS #
    @classmethod
    def validate_numbers_boundaries(cls, fieldName: str, value: int):
        """
        Performs a basic validation of boundaries for a int field
        """
        minVal = cls.numbersBoundaries[fieldName]["min"]
        maxVal = cls.numbersBoundaries[fieldName]["max"]

        if (minVal > value > maxVal):
            raise ValueError(f"{fieldName} value must be between {minVal} and {maxVal}")
        
        return value
    

    @classmethod
    def validate_list_values(cls, fieldName: str, valuesList: list[str]):
        """
        Performs a basic validation checking if the str values in a list exist in the game.
        e.g. check if list of equipment actually consists of the items that exist in the game
        """
        count = {
            "ankhSilver": 0,
            "ankhGolden": 0,
        }

        for value in valuesList:
            # check if the list holds an invalid value
            if not value in cls.validListValues[fieldName]:
                raise ValueError(f"Invalid value '{value}' found for {fieldName}")
            
            # count occurences of items that are allowed to be duplicates
            if value == 'ankhSilver' or value == 'ankhGolden':
                count[value] += 1


        # check if the list holds duplicates
        valuesSet = set(valuesList)
        if count["ankhGolden"] > 1 and count["ankhSilver"] > 1:
            if (len(valuesSet) != (len(valuesList) - count["ankhGolden"] - count["ankhSilver"] - 2)):
                raise ValueError(f"Found invalid duplicates of values")
        elif count["ankhGolden"] > 1:
            if (len(valuesSet) != (len(valuesList) - count["ankhGolden"] - 1)):
                raise ValueError(f"Found invalid duplicates of values")
        elif count["ankhSilver"] > 1:
            if (len(valuesSet) != (len(valuesList) - count["ankhSilver"] - 1)):
                raise ValueError(f"Found invalid duplicates of values")
        
        if len(valuesSet) != len(valuesList):
            raise ValueError(f"Found invalid duplicates of values")
            
        return valuesList
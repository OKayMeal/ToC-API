from pydantic import BaseModel
from typing import ClassVar

class ParentModel(BaseModel):
    numbersBoundaries: ClassVar[dict[str, dict[str, int]]] = {
        "field": {
            "min": 0,
            "max": 1
        },
    }
    validListValues: ClassVar[dict[str, list[str]]] = {
        "field": ['value1', 'value2']
    }

    # GENERIC VALIDATING METHODS #
    @classmethod
    def validate_numbers_boundaries(cls, fieldName: str, value: int):
        """
        Performs a basic validation of boundaries for a int field
        """
        minVal = cls.numbersBoundaries[fieldName]["min"]
        maxVal = cls.numbersBoundaries[fieldName]["max"]

        if (value < minVal or value > maxVal):
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
            if (len(valuesSet) != (len(valuesList) - count["ankhGolden"] - count["ankhSilver"] + 2)): # + 2 to account for two ankhs
                raise ValueError(f"Found invalid duplicates of values")
        elif count["ankhGolden"] > 1:
            if (len(valuesSet) != (len(valuesList) - count["ankhGolden"] + 1)): # +1 to account for 1 ankh that should stay
                raise ValueError(f"Found invalid duplicates of values")
        elif count["ankhSilver"] > 1:
            if (len(valuesSet) != (len(valuesList) - count["ankhSilver"] + 1)): # +1 to account for 1 ankh that should stay
                raise ValueError(f"Found invalid duplicates of values")
        else:
            if len(valuesSet) != len(valuesList):
                raise ValueError(f"Found invalid duplicates of values")
        
            
        return valuesList
    

    # @classmethod
    # def validate_time(cls, )
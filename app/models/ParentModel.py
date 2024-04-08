from datetime import datetime
import re
from pydantic import BaseModel
from typing import Any, ClassVar

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


    # DATA CLEANUP METHODS #
    @classmethod
    def clean_data(cls, modelDict: dict[str, Any]):
        for field, value in modelDict.items():
            # convert all boolean fields to ints
            if isinstance(value, bool):
                modelDict[field] = int(value)
            
            # add current date
            if field == 'date':
                modelDict[field] = cls.add_current_date()

            # turn all arrays into single strings
            if isinstance(value, list):                
                modelDict[field] = cls.convert_array_to_string(modelDict[field])
            
        return modelDict
    

    @classmethod
    def convert_array_to_string(cls, array: list[str] | list[int]) -> str:
        """
        Converts arrays of strings or integers to a single string with ', ' as delimiter
        """
        singleStr = ''
        if array == []:
            return singleStr
        
        for index, item in enumerate(array):
            if isinstance(item, int):
                item = str(item)
                
            singleStr += item
            if index != len(array) - 1:
                singleStr += ', '

        return singleStr
        

    @classmethod
    def add_current_date(cls):
        """
        Returns a current date in a string format 'YYYY-MM-DD HH:MM'
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M')


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
    

    @classmethod
    def validate_time(cls, time: str):
        """
        Performs a basic validation of time string
        """
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
    

    @classmethod
    def validate_string_length(cls, fieldName: str, string: str, maxLength: int, canBeEmpty: bool = False):
        """
        Performs a basic validation of string length
        """
        if len(string) > maxLength:
            raise ValueError(f'{fieldName} cannot be longer than {maxLength} characters')
         
        if (not canBeEmpty and len(string) == 0):
            raise ValueError(f'{fieldName} cannot be empty')
        
        return string
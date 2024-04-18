import pytest
from app.models.HighScore import HighScore

# validate_numbers_boundaries tests #
def test_validate_numbers_boundaries_valid_input():
    validInputs = HighScore.numbersBoundaries

    for field in validInputs:
        for case in validInputs[field]: 
            inputVal = validInputs[field][case]
            result = HighScore.validate_numbers_boundaries(field, inputVal)
            assert result == inputVal, f"""
                Result should be equal to the input value for valid input, Input: {inputVal}/ Result: {result} 
            """
    

def test_validate_numbers_boundaries_invalid_input():
    validInputs = HighScore.numbersBoundaries

    for field in validInputs:
        for case in validInputs[field]:
            inputVal = validInputs[field][case]
            if case == 'min':
                inputVal -= 1 # check value outside of the boundary
            elif case == 'max':
                inputVal += 1 # check value outside of the boundary
            
            with pytest.raises(ValueError) as excinfo:
                result = HighScore.validate_numbers_boundaries(field, inputVal)

            assert "value must be between" in str(excinfo.value)
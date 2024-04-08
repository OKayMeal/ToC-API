import pytest
from app.models.HighScore import HighScore

def test_validate_string_length_valid_input():
    validInputs = [
        {
            "string": 'testString12341', 
            "maxLength": 15, # exactly the len of str
            "canBeEmpty": False,
        },
        {
            "string": 'testString%!@&"', 
            "maxLength": 16, # len + 1
            "canBeEmpty": True,
        },
        {
            "string": '', 
            "maxLength": 10,
            "canBeEmpty": True,
        },
    ]

    for testDataSet in validInputs:
        result = HighScore.validate_string_length(
            'mockFieldName', testDataSet["string"], testDataSet["maxLength"], testDataSet["canBeEmpty"]
        )
        assert result == testDataSet["string"], "Valid inputs should stay the same after validation"
    

def test_validate_string_length_invalid_input():
    invalidInputs = [
        {
            "string": 'testString12341', 
            "maxLength": 14, # len of str - 1
            "canBeEmpty": False,
        },
        {
            "string": 'testString%!@&"', 
            "maxLength": 13, # len -2
            "canBeEmpty": True,
        },
        {
            "string": '', 
            "maxLength": 10,
            "canBeEmpty": False,
        },
        {
            "string": '12abc', 
            "maxLength": 0,
            "canBeEmpty": False,
        },
    ]

    for testDataSet in invalidInputs:
        with pytest.raises(ValueError) as excinfo:
            HighScore.validate_string_length(
                'mockFieldName', testDataSet["string"], testDataSet["maxLength"], testDataSet["canBeEmpty"]
            )
        assert 'cannot be longer than' or 'cannot be empty' in str(excinfo.value)
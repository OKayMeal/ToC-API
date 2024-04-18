import pytest
from app.models.HighScore import HighScore

# validate_list_values tests #
def test_validate_list_values_valid_values():
    valuesLists = {
        "bosses_defeated": {
            "oneValidBoss": ['pharaoh'],
            "twoValidBosses": ['ancientScarab', 'pharaoh'],
            "emptyList": [],
        },
        "equipment": {
            "oneValidItem": ['BootsOfHaste'],
            "twoValidItems": ['BootsOfHaste', 'FireSword'],
            "manyValidItems": ['BootsOfHaste', 'FireSword', 'NobleArmor', 'ankhGolden'],
        },
    }

    for suite in valuesLists:
        for case in valuesLists[suite]:
            inputVals = valuesLists[suite][case]
            result = HighScore.validate_list_values(suite, inputVals)

            assert result == inputVals, f"""
                Result should be the same as input. Result: {result} / Input: {inputVals}
            """


def test_validate_list_values_invalid_value_in_list():
    valuesList = ['NonexistentItem', 'FireSword', 'NobleArmor']
    with pytest.raises(ValueError) as excinfo:
        HighScore.validate_list_values('equipment', valuesList)
    
    assert "Invalid value" in str(excinfo.value)


def test_validate_list_values_not_allowed_duplicates():
    valuesList = ['FireSword', 'FireSword', 'NobleArmor']
    with pytest.raises(ValueError) as excinfo:
        HighScore.validate_list_values('equipment', valuesList)
    
    assert "invalid duplicates" in str(excinfo.value)


def test_validate_list_values_one_allowed_duplicate_and_no_not_allowed_duplicates():
    valuesLists = {
        "ankhGolden": ['ankhGolden', 'ankhGolden', 'FireSword'],
        "ankhSilver": ['ankhSilver', 'ankhSilver', 'FireSword']
    }
    
    for valuesList in valuesLists:
        result = HighScore.validate_list_values('equipment', valuesLists[valuesList])
        assert len(result) == len(valuesLists[valuesList]), f"""
            Allowed duplicates handled incorrectly. Values before: {valuesLists[valuesList]} / Values after: {result}
        """


def test_validate_list_values_many_allowed_duplicates_and_no_not_allowed_duplicates():
    valuesLists = {
        "ankhGolden": ['ankhGolden', 'ankhGolden', 'ankhGolden', 'FireSword'],
        "ankhSilver": ['ankhSilver', 'ankhSilver', 'ankhSilver', 'ankhSilver', 'FireSword']
    }
    for valuesList in valuesLists:
        result = HighScore.validate_list_values('equipment', valuesLists[valuesList])
        assert len(result) == len(valuesLists[valuesList]), f"""
            Allowed duplicates handled incorrectly. Values before: {valuesLists[valuesList]} / Values after: {result}
        """


def test_validate_list_values_one_allowed_duplicate_and_not_allowed_duplicates():
    valuesLists = {
        "ankhGolden": ['ankhGolden', 'ankhGolden', 'FireSword', 'FireSword'],
        "ankhSilver": ['ankhSilver', 'ankhSilver', 'FireSword', 'FireSword']
    }
    with pytest.raises(ValueError) as excinfo:
        for valuesList in valuesLists:
            HighScore.validate_list_values('equipment', valuesLists[valuesList])
    
    assert "invalid duplicates" in str(excinfo.value)


def test_validate_list_values_many_allowed_duplicates_and_not_allowed_duplicates():
    valuesLists = {
        "ankhGolden": ['ankhGolden', 'ankhGolden', 'ankhGolden', 'ankhGolden', 'NobleArmor', 'NobleArmor'],
        "ankhSilver": ['ankhSilver', 'ankhSilver', 'ankhSilver', 'NobleArmor', 'NobleArmor']
    }
    with pytest.raises(ValueError) as excinfo:
        for valuesList in valuesLists:
            HighScore.validate_list_values('equipment', valuesLists[valuesList])
    
    assert "invalid duplicates" in str(excinfo.value)


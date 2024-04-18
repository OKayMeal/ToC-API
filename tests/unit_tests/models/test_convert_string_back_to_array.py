from app.models.HighScore import HighScore

def test_convert_string_back_to_array_stringarr():
    singleStr = 'Item, AnotherItem, DifferentItem'
    result = HighScore.convert_string_back_to_array(singleStr, ', ')
    expectedArr = ['Item', 'AnotherItem', 'DifferentItem']

    assert result == expectedArr, f"String reconverted incorrectly to an array of strings. singleStr: {singleStr}. Expected outcome: {expectedArr}. Actual outcome: {result}"


def test_convert_string_back_to_array_intarr():
    singleStr = '2, 15, 239'
    result = HighScore.convert_string_back_to_array(singleStr, ', ')
    expectedArr = [2, 15, 239]

    assert result == expectedArr, f"String reconverted incorrectly to an array of ints. singleStr: {singleStr}. Expected outcome: {expectedArr}. Actual outcome: {result}"


def test_convert_string_back_to_array_emptyarr():
    singleStr = ''
    result = HighScore.convert_string_back_to_array(singleStr, ', ')
    expectedArr = []

    assert result == expectedArr, f"Empty string reconverted incorrectly to an empty array. singleStr: {singleStr}. Expected outcome: {expectedArr}. Actual outcome: {result}"


def test_convert_string_back_to_array_mixedarr():
    singleStr = 'Item, 2, 15'
    result = HighScore.convert_string_back_to_array(singleStr, ', ')
    expectedArr = ['Item', 2, 15]

    assert result == expectedArr, f"String reconverted incorrectly to a mixedd arr of str and ints. singleStr: {singleStr}. Expected outcome: {expectedArr}. Actual outcome: {result}"
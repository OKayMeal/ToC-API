from app.models.HighScore import HighScore

def test_convert_array_to_string_stringarr():
    arr = ['string1', ',string2,', 'loooooongstring3']
    expectedStr = "string1, ,string2,, loooooongstring3"
    arrStr = HighScore.convert_array_to_string(arr)
    
    assert arrStr == expectedStr, f"Result {arrStr} does not match the expected result {expectedStr}"


def test_convert_array_to_string_intarr():
    arr = [2, 3, 16]
    expectedStr = "2, 3, 16"
    arrStr = HighScore.convert_array_to_string(arr)
    
    assert arrStr == expectedStr, f"Result {arrStr} does not match the expected result {expectedStr}"


def test_convert_array_to_string_emptyarr():
    arr = []
    expectedStr = ""
    arrStr = HighScore.convert_array_to_string(arr)
    
    assert arrStr == expectedStr, f"Result {arrStr} does not match the expected result '' - empty string"


def test_convert_array_to_string_mixedarr():
    arr = ['teststr', 2, 'strtrrr', 163]
    expectedStr = "teststr, 2, strtrrr, 163"
    arrStr = HighScore.convert_array_to_string(arr)
    
    assert arrStr == expectedStr, f"Result {arrStr} does not match the expected result {expectedStr}"
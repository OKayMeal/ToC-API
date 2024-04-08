import pytest
from app.models.HighScore import HighScore

def test_validate_time_valid_format():
    validTimeFormats = ['19:15:04', '12:10:08', '16:18:21', '21:20:30']

    for validTimeFormat in validTimeFormats:
        result = HighScore.validate_time(validTimeFormat)
        assert result == validTimeFormat, 'Valid time string should stay the same after validation'


def test_validate_time_invalid_format():
    invalidTimeFormats = ['19-15-04', '12.10.08', '16/18/21', '21:20:30:15', '1:1:1']

    for invalidTimeFormat in invalidTimeFormats:
        with pytest.raises(ValueError) as excinfo:
            HighScore.validate_time(invalidTimeFormat)
        
        assert 'HH:MM:SS format' in str(excinfo.value)


def test_validate_time_invalid_hours():
    invalidHours = ['24:00:00', '25:00:00']

    for invalidHour in invalidHours:
        with pytest.raises(ValueError) as excinfo:
            HighScore.validate_time(invalidHour)
        
        assert 'between 00 and 23' in str(excinfo.value)


def test_validate_time_invalid_minutes_or_seconds():
    invalidMinutesOrSeconds = ['22:61:00', '22:00:62']

    for invalidValue in invalidMinutesOrSeconds:
        with pytest.raises(ValueError) as excinfo:
            HighScore.validate_time(invalidValue)
        
        assert 'between 00 and 59' in str(excinfo.value)

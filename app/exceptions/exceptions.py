"""
Custom exceptions
"""

class DatabaseConnectionError(Exception):
    """Custom exception for database connection failures."""
    pass


class FileNotFoundError(Exception):
    """Custom exception for file loading failures."""
    pass

class WrongFileFormat(Exception):
    """Custom exception for wrong file format."""
    pass


class KeyExpired(Exception):
    """Custom exception for an expired key."""
    pass
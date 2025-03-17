import re
from datetime import datetime




def bytes_to_string(byte_data, encoding='utf-8', errors='replace'):
    """
    Converts bytes data to a string.

    Args:
        byte_data: The bytes data to convert.
        encoding: The encoding to use (default: 'utf-8').
        errors: How to handle encoding errors (default: 'replace').

    Returns:
        The string representation of the bytes data, or None if input is not bytes.
    """
    if isinstance(byte_data, bytes):
        try:
            return byte_data.decode(encoding, errors=errors)
        except UnicodeDecodeError as e:
            print(f"Error decoding bytes: {e}")
            return None
    else:
        print("Input is not of type bytes")
        return None
 
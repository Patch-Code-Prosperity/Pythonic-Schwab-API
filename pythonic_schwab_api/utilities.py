"""
Utility functions for handling parameter cleaning, datetime conversion, and list formatting.
"""

def clean_params(params):
    """
    Remove None values from a dictionary of parameters.

    Args:
        params (dict): Dictionary of parameters.

    Returns:
        dict: Dictionary with None values removed.
    """
    return {k: v for k, v in params.items() if v is not None}


def convert_time(dt=None, format_type="8601"):
    """
    Convert datetime objects into a string format according to a specified type.

    Args:
        dt (datetime, optional): The datetime object to convert. Defaults to None.
        format_type (str, optional): The format type to convert to. Defaults to "8601".

    Returns:
        str or int: The formatted datetime string or epoch time in milliseconds.
    """
    if dt is None:
        return None

    formats = {
        "8601": lambda x: x.isoformat()[:-3] + 'Z',  # ISO8601 format
        "epoch": lambda x: int(x.timestamp() * 1000),  # Epoch time in milliseconds
        "YYYY-MM-DD": lambda x: x.strftime("%Y-%m-%d")  # Custom Schwab Options date format
    }
    formatter = formats.get(format_type, str)
    return formatter(dt)


def format_list(items):
    """
    Convert a list of items into a comma-separated string or return single item as string.

    Args:
        items (list or any): The list of items to format or a single item.

    Returns:
        str: Comma-separated string of items or single item as string.
    """
    if items is None:
        return None
    return ",".join(items) if isinstance(items, list) else str(items)

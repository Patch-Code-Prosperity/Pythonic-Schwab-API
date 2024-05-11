class ParameterParser:
    @staticmethod
    def clean_params(params):
        """
        Removes None values from a dictionary of parameters.
        This ensures that only valid parameters are sent in API requests.
        
        Parameters:
            params (dict): A dictionary containing parameter names and values.
        
        Returns:
            dict: A dictionary with all None values removed.
        """
        return {k: v for k, v in params.items() if v is not None}

class DateTimeConverter:
    @staticmethod
    def convert_time(dt=None, format_type="8601"):
        """
        Converts datetime objects into a string format according to a specified format type.
        Supports ISO 8601, epoch time in milliseconds, and custom date formats.

        Parameters:
            dt (datetime.datetime, optional): The datetime object to convert. Defaults to None.
            format_type (str, optional): The type of format to convert the datetime into. 
                Supported types are "8601" for ISO8601 format, "epoch" for epoch time in milliseconds, 
                and "YYYY-MM-DD" for custom date format. Defaults to "8601".

        Returns:
            str or int: The formatted date string or integer (for epoch), or None if dt is None.
        """
        if dt is None:
            return None

        formats = {
            "8601": lambda x: x.isoformat()[:-3] + 'Z',  # Reduces to milliseconds and appends 'Z' to denote UTC time
            "epoch": lambda x: int(x.timestamp() * 1000),  # Converts to milliseconds since the Unix epoch
            "YYYY-MM-DD": lambda x: x.strftime("%Y-%m-%d")  # Formats date as YYYY-MM-DD
        }
        return formats.get(format_type, lambda x: x)(dt)

def format_list(items):
    """
    Converts a list of items into a comma-separated string. If the input is not a list, it returns the input as is.
    This is used to format lists for parameters in API requests where multiple values can be passed as comma-separated.

    Parameters:
        items (list or str): A list of items or a single string item.

    Returns:
        str: A comma-separated string if items is a list, otherwise the original input string.
    """
    if items is None:
        return None
    return ",".join(items) if isinstance(items, list) else items

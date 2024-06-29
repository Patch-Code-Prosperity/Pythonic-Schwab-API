"""
This module provides utility functions for constructing request dictionaries
for Schwab's streaming API.
"""

def basic_request(service, request_id, command, customer_id, correl_id, parameters=None):
    """
    Constructs a basic request dictionary for streaming commands.

    Args:
        service (str): The service name, e.g., 'ADMIN'.
        request_id (int): The identifier for this request.
        command (str): The command to be executed, e.g., 'LOGIN'.
        customer_id (str): The Schwab client customer ID.
        correl_id (str): The Schwab client correlation ID.
        parameters (dict, optional): Additional parameters for the command.

    Returns:
        dict: The request dictionary.
    """
    request = {
        "service": service.upper(),
        "requestid": str(request_id),
        "command": command.upper(),
        "SchwabClientCustomerId": customer_id,
        "SchwabClientCorrelId": correl_id
    }
    # Include parameters if provided
    if parameters:
        request["parameters"] = parameters
    return request

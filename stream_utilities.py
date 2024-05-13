def basic_request(service, command, request_id, parameters=None):
    return {
        "service": service.upper(),
        "command": command.upper(),
        "requestid": request_id,
        "parameters": parameters if parameters else {}
    }

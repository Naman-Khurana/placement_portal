def success_response(message , status_code=200, **extra):
    response={
        "message" : message,
    }
    response.update(extra)
    return response,status_code

def error_response(message,status_code=400,**extra):
    response={
        "error" : message
    }
    response.update(extra)
    return response,status_code
def response_out(message, status_code, results=None) -> dict:
    response_obj = {
        "message": message,
        "status_code": status_code,
    }

    if(results is not None):
        response_obj["result"] = results

    return response_obj
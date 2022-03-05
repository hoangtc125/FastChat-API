
def ResponseModel(data, token, message):
    return {
        "data": [data],
        "token": token,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
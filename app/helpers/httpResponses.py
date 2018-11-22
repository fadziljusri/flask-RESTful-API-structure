from flask_restful import abort

# 2xx Success
def Res200(data, message=None):
    return {
        "status": "success",
        "data": data,
        "message": message or "OK"
    }, 200

def Res201(data, message=None):
    return {
        "status": "success",
        "data": data,
        "message": message or "Created"
    }, 201

def Res204(message=None):
    return {
        "status": "success",
        "data": None,
        "message": message or "No Content"
    }, 204

# 4xx Client Errors
status = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Conflict",
}

def Abort(code, message=None):
    return abort(
        code,
        status="failed",
        data=None,
        message=message or status.get(code, "Error")
    )
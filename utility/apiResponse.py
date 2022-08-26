import json

def apiSuccess(statusCode,message,data):
    return {"statusCode":statusCode, "message" : message, "data": json.dump(data)}


def apiError(statusCode,message):
    return {"statusCode":statusCode, "message" : message}
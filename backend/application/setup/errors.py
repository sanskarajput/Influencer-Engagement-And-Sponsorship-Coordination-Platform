from flask import make_response
from werkzeug.exceptions import HTTPException
import json



# not found
class ResourceNotFoundError(HTTPException):
    def __init__(self, status_code=404, error_code="NOT_FOUND", error_message="Resource not found"):
        message = {
            "error_code": error_code,
            "error_message": error_message
        }
        self.response = make_response(json.dumps(message), status_code)

class UserNotFoundError(HTTPException):
    def __init__(self, status_code=404, error_code="USER_NOT_FOUND", error_message="User not found"):
        message = {
            "error_code": error_code,
            "error_message": error_message
        }
        self.response = make_response(json.dumps(message), status_code)




# already exists
class ResourceAlreadyExists(HTTPException):  
    def __init__(self, status_code=409, error_code="ALREADY_EXISTS", error_message="Resource already exists"):
        message = {
            "error_code": error_code,
            "error_message": error_message
        }
        self.response = make_response(json.dumps(message), status_code)

class UserAlreadyExists(HTTPException):  
    def __init__(self, status_code=409, error_code="USER_ALREADY_EXISTS", error_message="User already exists"):
        message = {
            "error_code": error_code,
            "error_message": error_message
        }
        self.response = make_response(json.dumps(message), status_code)




class BadRequest(HTTPException):
    def __init__(self, status_code=400, error_code="BAD_REQUEST", error_message="Invalid request"):
        message = {
            "error_code": error_code,
            "error_message": error_message
        }  
        self.response = make_response(json.dumps(message), status_code)



class OwnershipRequired(HTTPException):
    def __init__(self, status_code=403, error_code="OWNERSHIP_REQUIRED", error_message="Ownership required"):
        message = {
            "error_code": error_code,
            "error_message": error_message
        }
        self.response = make_response(json.dumps(message), status_code)



class InternalServerError(HTTPException):
    def __init__(self, status_code=500, error_code="INTERNAL_SERVER_ERROR", error_message="Internal server error"):
        message = {
            "error_code": error_code,
            "error_message": error_message
        }
        self.response = make_response(json.dumps(message), status_code)
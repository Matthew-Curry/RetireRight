"""Utility methods to write HTTP responses"""

import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # if obj is decimal convert to string
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def write_response(status_code:int, body:str) -> dict:
    """write http response with CORS headers
    args:
        status_code (int): the status code to return in the HTTP response
        body (str): string representing the body of the response
    returns:
        Dictionary representing the response with needed CORS headers"""
    resp = {"statusCode": status_code, 
            "isBase64Encoded": False,
            'headers': {
                'Content-Type': "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        }
    
    if body:
        resp["body"] = body
    else:
        resp["body"] = ""

    return resp

def write_response_from_obj(status_code:int, body:dict) -> dict:
    """write http response with CORS headers given body as dictionary
    args:
        status_code (int): the status code to return in the HTTP response
        body (dict): dictionary representing the body of the response
    returns:
        Dictionary representing the response with needed CORS headers"""
    body_str = json.dumps(body, cls=DecimalEncoder)
    return write_response(status_code, body_str)

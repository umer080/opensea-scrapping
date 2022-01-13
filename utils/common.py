from flask import jsonify
from bson.objectid import ObjectId
import json


class JSONEncoder(json.JSONEncoder):
    """extend json-encoder class"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def custom_json_response(data=None, is_error=None, status_code=404, error_message=None):
    """
    This function is build to customize the json response
    and be consistence overall the Api's response.
    :param data:
    :param is_error:
    :param status_code:
    :param error_message:
    :return:
    """
    response = {
        "data": JSONEncoder().encode(data),
        "is_error": is_error,
        "status_code": status_code,
        "error_message": error_message
    }
    return jsonify(response)

from flask import jsonify, make_response
import json


def custom_json_response(data=None, error_message=None, status_code=404):
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
        "data": data,
        "error_message": error_message,
        "status_code": status_code
    }
    return make_response(jsonify(response), status_code)

from flask import Blueprint, jsonify


home = Blueprint("home", __name__)

WELCOME_MESSAGE = (
    "Welcome to the XLSForm to XForm API! Make a POST request to '/api/v1/convert' to convert an XLSForm "
    "to an ODK XForm."
)


@home.route("/")
def index():
    return jsonify(status=200, message=WELCOME_MESSAGE)

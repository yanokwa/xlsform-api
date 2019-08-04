from flask import Blueprint, jsonify


home = Blueprint("home", __name__)

WELCOME_MESSAGE = "Welcome to the XLSForm API! Make a POST request to '/api/v1/convert' to convert Excel " \
                  "forms to XForms that can be used with ODK systems."


@home.route("/")
def index():
    return jsonify(
        status=200,
        message=WELCOME_MESSAGE
    )

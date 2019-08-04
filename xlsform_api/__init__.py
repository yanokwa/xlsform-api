from flask import Flask
from xlsform_api.api.controllers import api
from xlsform_api.home.controllers import home

app = Flask(__name__)

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(api, url_prefix='/api/v1/')

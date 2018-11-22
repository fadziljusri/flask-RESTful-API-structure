from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
api = Api(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200/day", "50/hour", "3/minute"]
)

app.config['ERROR_404_HELP'] = False

from app.resources import *
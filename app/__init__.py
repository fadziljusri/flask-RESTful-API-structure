from flask import Flask, jsonify
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['ERROR_404_HELP'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

api = Api(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200/day", "50/hour"]
)
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'status': 'failed',
        'data': None,
        'message': 'The token has expired.',
        'refresh': True
    }), 401


from app.resources import *
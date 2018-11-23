from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity,
)
import datetime

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'status': 401,
        'msg': 'The token has expired.',
        'refresh': True
    }), 401


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    ret = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username)
    }
    return jsonify(ret), 200


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    # expires = datetime.timedelta(seconds=30)
    ret = {
        # 'access_token': create_access_token(identity=current_user, expires_delta=expires)
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


# @app.route('/api/token', methods=['POST'])
# @jwt_required
# def create_api_token():
#     username = get_jwt_identity()
#     token = create_access_token(username, expires_delta=False)
#     return jsonify({'token': token}), 201


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5253)
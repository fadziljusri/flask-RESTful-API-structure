from app import api, limiter
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
create_access_token,
create_refresh_token,
jwt_refresh_token_required,
get_jwt_identity
)

# import datetime

from app.helpers.httpResponses import (
Res200
)

class Auth(Resource):

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()

        username = args['username']

        # Use create_access_token() and create_refresh_token() to create our
        # access and refresh tokens
        data = {
            'access_token': create_access_token(identity=username),
            'refresh_token': create_refresh_token(identity=username)
        }
        return Res200(data)


class AuthTokenRefresh(Resource):
    decorators = [
        # limiter.limit('3/15minute')
        # limiter.exempt
    ]

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        # expires = datetime.timedelta(seconds=30) # expires = False
        ret = {
            # 'access_token': create_access_token(identity=current_user, expires_delta=expires)
            'access_token': create_access_token(identity=current_user)
        }

        return Res200(ret)


api.add_resource(Auth, '/auth')
api.add_resource(AuthTokenRefresh, '/auth/token/refresh')
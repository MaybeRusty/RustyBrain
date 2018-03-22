from flask_restful import request
from flask.globals import current_app
from flask_jwt import _jwt, JWTError
import datetime

from model.admin import Admin

def authenticate(username, password, user_type):
    ret = Admin.find_by_username(username)
    if ret.check() is False:
        return
    if ret.data and ret.data.confirm_password(password):
        if user_type == ret.data.login_type:
            return ret.data

def identity(payload):
    uuid = payload['identity']
    ret = Admin.find_by_uuid(uuid)
    if ret.check() is False:
        return
    else:
        return ret.data

def payload_handle(identity):
    iat = datetime.datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    identity = getattr(identity, 'uuid') or identity['uuid']
    return {'exp': exp, 'iat': iat, 'nbf': nbf, 'identity': identity}

def auth_request_handle():
    data = request.get_json()
    username    = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
    password    = data.get(current_app.config.get('JWT_AUTH_PASSWORD_KEY'), None)
    user_type   = data.get(current_app.config.get('JWT_AUTH_LOGIN_TYPE_KEY'), None)

    identity = _jwt.authentication_callback(username, password, user_type)

    if identity:
        access_token = _jwt.jwt_encode_callback(identity)
        return _jwt.auth_response_callback(access_token, identity)
    else:
        raise JWTError('Bad Request', 'Invalid credentials2')

auth_url_rule='/auth'
auth_url_options = {'methods': ['POST'],'view_func':auth_request_handle}

import json

from flask import Blueprint, request, make_response, jsonify, Response
from flask.views import MethodView

import ipdb # ipdb.set_trace()

from app import bcrypt, app
from app.models import User, BlacklistToken

auth_blueprint = Blueprint('auth', __name__)

# 注册接口
class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    def post(self):
        post_data = request.get_json()

        user = User.objects(phone=post_data.get('phone')).first()
        if not user:
            try:
                # 新增一个用户
                new_user = User()
                new_user.phone = post_data.get('phone')
                new_user.password = bcrypt.generate_password_hash(post_data.get('password'), app.config.get('BCRYPT_LOG_ROUNDS')).decode()
                new_user.save()

                # 生成一个auth token, 字节
                auth_token = User.encode_auth_token(str(new_user.id))
                responseObject = {
                    'status': 'success-成功',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }

                # method-1: support 中文
                return make_response(jsonify(responseObject)), 201

                # method-2: support 中文
                # return Response(
                #     response=json.dumps(responseObject),
                #     mimetype='application/json',
                #     status=201
                # )
            except Exception as e:
                app.logger.error(e)

                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401

        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

# 登录接口
class LoginAPI(MethodView):
    def post(self):
        # 获取参数
        post_data = request.get_json()
        try:
            user = User.objects(phone=post_data.get('phone')).first()
            if user:
                # 验证密码成功
                if bcrypt.check_password_hash(user.password, post_data.get('password')):
                    # 生成一个auth token, 字节
                    auth_token = User.encode_auth_token(str(user.id))
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'account or password is wrong.'
                    }
                    return make_response(jsonify(responseObject)), 404
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User don not exists.',
                }
                return make_response(jsonify(responseObject)), 404

        except Exception as e:
            app.logger.error(e)

            responseObject = {
                'status': 'fail',
                'message': 'System error.Try again'
            }
            return make_response(jsonify(responseObject)), 500


# 退出接口
# Authorization like: 'wakeup ' + auth_token
class LogoutAPI(MethodView):

    def delete(self):
        # 验证token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(' ')[1]
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    # 如果推出成功，则将该token写进BlacklistToken
                    blacklist_token = BlacklistToken()
                    blacklist_token.token = auth_token
                    blacklist_token.save()

                    # TODO something
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    app.logger.error(e)

                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200

            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints => 相当于注册路由到这个分组
auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/logout',
    view_func=logout_view,
    methods=['DELETE']
)
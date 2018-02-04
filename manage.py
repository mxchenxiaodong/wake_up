
import os

from flask_script import Manager
import ipdb

from app import app, bcrypt
from app.models import *


# 实例化
manager = Manager(app)

# 装饰器
@manager.command
def hello():
    print('hello world...')

# can use: python manage.py test_save_user
@manager.command
def test_save_user():
    user = User()
    user.phone = '18826418546'
    user.password = bcrypt.generate_password_hash('12345678', app.config.get('BCRYPT_LOG_ROUNDS')).decode()
    user.save()

@manager.command
def app_console():
    ipdb.set_trace()

if __name__ == '__main__':
  manager.run()

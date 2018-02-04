import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# 获取配置信息
# 从环境变量里面取，如果取不到，则使用默认开发配置
app_settings = os.getenv('APP_SETTINGS', 'app.config.DevelopmentConfig')

# 将对象转为配置信息
# can use: app.config['MONGODB_SETTINGS']
app.config.from_object(app_settings)

# MongoDB: 对应MONGODB_SETTINGS配置
db = MongoEngine(app)

# 有加密模块
bcrypt = Bcrypt(app)




# 将各个路由加进来
from app.auth.views import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')


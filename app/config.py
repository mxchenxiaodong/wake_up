
import os

# /Users/Don/python_project/code/wake_up/app
basedir = os.path.abspath(os.path.dirname(__file__))

# os.environ.get('SECRET_KEY', 'my_precious')
# os.getenv('SECRET_KEY', 'my_precious')
# 两者相等的
class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', '1a3d4267b254fbf9f2846375c6aa83dd')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/wake_up'
    }


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/wake_up'
    }

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False

    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost/wake_up'
    }
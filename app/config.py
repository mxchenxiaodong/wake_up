
import os

# /Users/Don/python_project/code/wake_up/app
basedir = os.path.abspath(os.path.dirname(__file__))

# os.environ.get('SECRET_KEY', 'my_precious')
# os.getenv('SECRET_KEY', 'my_precious')
# 两者相等的
class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGODB_DB'),
        'host': os.getenv('MONGODB_HOST'),
        'port': int(os.getenv('MONGODB_PORT')),
        'username': os.getenv('MONGODB_USERNAME'),
        'password': os.getenv('MONGODB_PASSWORD')
    }

    REDIS_SETTINGS = {
        'host': os.getenv('REDIS_HOST'),
        'port': os.getenv('REDIS_PORT'),
        'db': os.getenv('REDIS_DB'),
        'password': os.getenv('REDIS_PASSWORD'),
        'url': 'redis://[:{}]@{}:{}/{}'.format(os.getenv('REDIS_PASSWORD'), os.getenv('REDIS_HOST'), os.getenv('REDIS_PORT'), os.getenv('REDIS_DB'))
    }

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
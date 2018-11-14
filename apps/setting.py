import os
from redis import Redis


def get_prj_dir():
	return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "sqlite:///{}/devcms.db".format(get_prj_dir())
	SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_redis_address():
	return Redis(host='47.104.252.32', port=6379)


class DevConfig(BaseConfig):
	SESSION_TYPE = 'redis'
	SESSION_REDIS = get_redis_address()


class ProductConfig(BaseConfig):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:psd123456@47.104.252.32/homework"
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevAPIConfig(BaseConfig):
	SMS_LIFETIME = 300

	API_REDIS = get_redis_address()

	SECRET_KEY = 'elm_api'
	TOKEN_EXPIRES = 24 * 3600
	CART_LIFETIME = 3600

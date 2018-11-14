from flask import Flask
from flask_login import LoginManager
from flask_session import Session

login_manager = LoginManager()


def register_db(app):
	from apps.models import db
	db.init_app(app)


def register_bp(app):
	from apps.cms import cms_bp
	app.register_blueprint(cms_bp)


def create_app():
	app = Flask(__name__)
	app.config.from_object('apps.setting.DevConfig')
	Session(app)
	# 注册数据库
	register_db(app)
	# 注册蓝图
	register_bp(app)
	# 登录插件的注册
	login_manager.init_app(app=app)
	# 默认情况下，当未登录的用户尝试访问一个 login_required 装饰的视图，
	# Flask-Login 会闪现一条消息并且重定向到登录视图。
	# (如果未设置登录视图，它将会以 401 错误退出。)
	login_manager.login_view = 'cms.login'
	return app


def register_api_bp(app):
	from apps.apis import api_bp
	app.register_blueprint(api_bp)


def create_api_app():
	app = Flask(__name__, static_url_path="", static_folder="./web_client")
	app.config.from_object('apps.setting.DevAPIConfig')
	register_db(app)
	register_api_bp(app)
	return app

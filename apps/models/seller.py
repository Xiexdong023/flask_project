from apps.models import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from apps import login_manager


class CmsSellerModel(BaseModel, UserMixin):
	__tablename__ = "seller"
	username = db.Column(db.String(20), nullable=False, comment="用户名")
	__password = db.Column("password", db.String(128), nullable=False, comment="用户密码")

	@property
	def password(self):
		return self.__password

	@password.setter
	def password(self, val):
		self.__password = generate_password_hash(val)

	def check_password(self, data):
		return check_password_hash(self.password, data)


#  user_loader 回调,这个回调用于从会话中存储的用户 ID 重新加载用户对象。
# 它应该接受一个用户的 unicode ID(字符串ID) 作为参数，并且返回相应的用户对象
@login_manager.user_loader
def load_user(userid: str):
	# return SellerModel.query.filter_by(id=int(userid)).first()
	return CmsSellerModel.query.get(int(userid))

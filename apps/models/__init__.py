from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True, comment="ID")
	status = db.Column(db.Integer(), default=0, comment="是否删除")

	def set_attr(self, a1):
		"""使用内建函数setattr给对象添加或修改属性,可以解决(obj.属性)点(.)方法操作符不能接变量的情况"""
		for k, v in a1.items():
			if k != "repassword" and hasattr(self, k) and k != "id":
				setattr(self, k, v)

	def __getitem__(self, item):
		"""重写该方法,供dict(obj)使用,该魔术方法配合 keys()函数使用 将一个对象指定属性转成字典"""
		if hasattr(self, item):
			return getattr(self, item)


from apps.models.seller import CmsSellerModel
from apps.models.shop_view import ShopModel
from apps.models.buyer import BuyerUser, BuyerAddress

from apps.models import BaseModel, db


class ShopModel(BaseModel):
	__tablename__ = "sellershop"
	pub_id = db.Column(db.String(16), unique=True, index=True, comment="外部ID")
	shop_name = db.Column(db.String(32), unique=True, nullable=False, comment="店铺名")
	shop_img = db.Column(db.String(128), default="", comment="店铺图片")
	shop_rating = db.Column(db.Float, default=5.0, comment="店铺评分")
	brand = db.Column(db.Boolean, default=False, comment="是否是品牌")
	on_time = db.Column(db.Boolean, default=True, comment="是否准时送达")
	fengniao = db.Column(db.Boolean, default=True, comment="是否蜂鸟配送")
	bao = db.Column(db.Boolean, default=False, comment="是否保险")
	piao = db.Column(db.Boolean, default=True, comment="是否有发票")
	zhun = db.Column(db.Boolean, default=False, comment="是否准标识")
	start_send = db.Column(db.Float, default=0.0, comment="起送价格")
	send_cost = db.Column(db.Float, default=0.0, comment="配送费")
	notice = db.Column(db.String(210), default='', comment="店铺公告")
	discount = db.Column(db.String(210), default='', comment="优惠信息")
	seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), comment="商家")
	seller = db.relationship("CmsSellerModel", backref="shop")

	def keys(self):
		return "shop_name", "shop_img", "brand", "on_time", "fengniao", "bao", \
		       "piao", "zhun", "start_send", "send_cost", "notice", "discount"


# 店铺菜品分类表
class MenuCategory(BaseModel):
	__tablename__ = "menucate"
	# 分类名称
	name = db.Column(db.String(32))
	# 分类描述
	description = db.Column(db.String(128), default='')
	# 分类编号
	type_accumulation = db.Column(db.String(16))
	# 是否默认
	is_default = db.Column(db.Boolean, default=False)
	# 归属店铺
	shop_pid = db.Column(db.String(16), db.ForeignKey('sellershop.pub_id'))

	shop = db.relationship('ShopModel', backref='categories')

	def keys(self):
		return "name", "description", "type_accumulation", "is_default"


class GoodsModel(BaseModel):
	__tablename__ = "goods"
	goods_name = db.Column(db.String(32), nullable=False, comment="菜品名")
	cate_id = db.Column(db.String, db.ForeignKey('menucate.id'))
	goods_price = db.Column(db.Float, nullable=False, comment="菜品价格")
	description = db.Column(db.String(128), nullable=False, comment="菜品描述")
	tips = db.Column(db.String(128), nullable=False, comment="菜品提示信息")
	goods_img = db.Column(db.String(128), default='', comment="菜品图片")
	goods_sales = db.Column(db.Integer, default=0, comment="菜品销量")
	goods_rating = db.Column(db.Float, default=5.0, comment="菜品评分")
	cate = db.relationship('MenuCategory', backref='goods')

	def keys(self):
		return "goods_id", "goods_name", "rating", "goods_price", "description", "tips", "month_sales", "goods_img"

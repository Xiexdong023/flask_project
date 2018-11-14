from wtforms import Form, StringField, BooleanField, DecimalField, HiddenField, validators, FloatField, SelectField
from apps.models.shop_view import ShopModel, MenuCategory
from flask import request


class ShopForm(Form):
	shop_name = StringField(label="店铺名称", validators=[validators.DataRequired(message="必填"), ],
	                        render_kw={'class': 'form-control', 'placeholder': '请输入店铺名称'}, )
	brand = BooleanField(label="是否品牌")
	on_time = BooleanField(label="是否准时送达")
	fengniao = BooleanField(label="是否蜂鸟配送")
	bao = BooleanField(label="是否保险")
	piao = BooleanField(label="发票")
	zhun = BooleanField(label="是否准标识")
	start_send = DecimalField(label="起送价格", render_kw={'class': 'form-control', 'placeholder': "起送价格"})
	send_cost = DecimalField(label="配送费", render_kw={'class': 'form-control', 'placeholder': "配送费"})
	notice = StringField(label="店铺公告", render_kw={'class': 'form-control', 'placeholder': "店铺公告"})
	discount = StringField(label="优惠信息", render_kw={'class': 'form-control', 'placeholder': "优惠信息"})
	shop_img = StringField(label="店铺图片", id='image-input')

	def validate_shop_name(self, obj):
		s1 = ShopModel.query.filter_by(shop_name=obj.data).first()
		if s1 and request.url_rule.rule == "/add_shop/":
			raise validators.ValidationError(message="店铺已存在")

	def validate_start_send(self, obj):
		obj.data = float('{:.2f}'.format(obj.data))

	def validate_send_cost(self, obj):
		obj.data = float('{:.2f}'.format(obj.data))


class CateForm(Form):
	# 菜品名称
	name = StringField(label="菜品分类名", validators=[validators.DataRequired(message="请输入菜品分类名"),
	                                              validators.Length(max=32, message="不能超过32字符"), ],
	                   render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类名'},
	                   )
	# 分类描述
	description = StringField(label="菜品分类描述", validators=[validators.Length(max=128, message="不能超过128字符"), ],
	                          render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类描述'},
	                          )
	# 分类编号
	type_accumulation = StringField(label="菜品分类编号",
	                                validators=[validators.Length(max=16, message="不能超过16字符"),
	                                            validators.DataRequired(message="必填")],
	                                render_kw={'class': 'form-control', 'placeholder': '请输入菜品分类编号'},
	                                )
	# 是否默认
	is_default = BooleanField(label="是否默认")

	def validate_name(self, obj):
		if MenuCategory.query.filter_by(name=obj.data).first():
			raise validators.ValidationError(message="菜品分类名已存在")

	def validate_type_accumulation(self, obj):
		if MenuCategory.query.filter_by(type_accumulation=obj.data).first():
			raise validators.ValidationError(message="菜品分类编号重复")


class GoodsForm(Form):
	goods_name = StringField(label="菜品名称", validators=[validators.DataRequired(message="请输入菜品名称"),
	                                                   validators.Length(max=32, message="不能超过32字符"), ],
	                         render_kw={'class': 'form-control', 'placeholder': '请输入菜品名称'},
	                         )
	cate_id = SelectField(label="菜品分类名", coerce=str, render_kw={'class': 'form-control'},
	                      )
	goods_price = DecimalField(label="菜品价格", validators=[validators.DataRequired(message="请输入菜品价格"), ],
	                           render_kw={'class': 'form-control', 'placeholder': '请输入菜品价格'},
	                           )
	# 描述
	description = StringField(label="菜品描述", validators=[validators.Length(max=128, message="不能超过128字符"), ],
	                          render_kw={'class': 'form-control', 'placeholder': '请输入菜品描述'},
	                          )
	tips = StringField(label="菜品提示信息", validators=[validators.Length(max=128, message="不能超过128字符"), ],
	                   render_kw={'class': 'form-control', 'placeholder': '请输入提示信息'},
	                   )
	goods_image = StringField(label="菜品图片", id="image-input")

	def __init__(self, pub_id, *args, **kwargs):
		super(GoodsForm, self).__init__(*args, **kwargs)
		# self.category_id.choices = [(1,'a')]
		shop = ShopModel.query.filter_by(pub_id=pub_id).first()
		self.cate_id.choices = [(str(cate.id), cate.name) for cate in shop.categories]


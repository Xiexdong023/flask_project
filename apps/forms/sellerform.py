from flask import request
from wtforms import Form, StringField, PasswordField, validators

from apps.models import CmsSellerModel


class SellerLoginForm(Form):
	username = StringField(label="",
	                       validators=[validators.DataRequired(message="必填"),
	                                   validators.length(min=3, message="必须大于3个字符"),
	                                   validators.length(max=10, message="必须少于10个字符")
	                                   ],
	                       render_kw={'class': 'form-control', 'placeholder': '用户名'}
	                       )
	password = PasswordField(label="",
	                         validators=[validators.DataRequired(message="必填"),
	                                     validators.length(min=4, message="必须大于4个字符"),
	                                     validators.length(max=16, message="必须少于16个字符"),
	                                     ],
	                         render_kw={'class': 'form-control', 'placeholder': '登录密码'}
	                         )


# def validate_username(self, obj):
# 	if request.url_rule.rule == '/login/':
# 		# obj.data username输入框的字符串
# 		seller = CmsSellerModel.query.filter_by(username=obj.data).first()
# 		if seller is None:
# 			raise validators.ValidationError(message="用户不存在")
# 		elif getattr(seller, "password") != self.password.data:
# 			raise validators.ValidationError(message="账号或密码错误")


class SellerRegisterForm(SellerLoginForm):
	repassword = PasswordField(label="",
	                           validators=[validators.DataRequired(message="必填"),
	                                       validators.EqualTo("password", message="两次输入密码不一致")
	                                       ],
	                           render_kw={'class': 'form-control', 'placeholder': '确认密码'}
	                           )

	def validate_username(self, obj):
		# obj.data username输入框的字符串
		seller = CmsSellerModel.query.filter_by(username=obj.data).first()
		if seller:
			raise validators.ValidationError(message="用户已存在")

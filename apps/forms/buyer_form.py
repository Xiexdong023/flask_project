from wtforms import Form, StringField, validators, IntegerField
from flask import current_app
from apps.models.buyer import BuyerUser


class BuyerLoginForm(Form):
	name = StringField(
		validators=[
			validators.DataRequired(message="请输入用户名信息"),
			validators.Length(min=3, message="用户名不能少于3个字符"),
			validators.Length(max=32, message="用户名不能超过32个字符"),
		],
	)
	# 买家密码
	password = StringField(
		validators=[
			validators.DataRequired(message="请输入密码"),
			validators.Length(min=3, message="密码不能少于3个字符"),
			validators.Length(max=16, message="密码不能超过16个字符"),
		],
	)


class BuyerRegisterForm(Form):
	username = StringField(
		validators=[
			validators.DataRequired(message="请输入用户名信息"),
			validators.Length(min=3, message="用户名不能少于3个字符"),
			validators.Length(max=32, message="用户名不能超过32个字符"),
		],
	)
	# 买家密码
	password = StringField(
		validators=[
			validators.DataRequired(message="请输入密码"),
			validators.Length(min=3, message="密码不能少于3个字符"),
			validators.Length(max=16, message="密码不能超过16个字符"),
		],
	)
	# 买家电话号码
	tel = StringField(
		validators=[
			validators.DataRequired(message="请输入电话号码"),
			validators.Regexp(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18['
			                  r'0-9])|166|198|199)\d{8}$', message="请输入正确的电话号码"),
		],
	)
	# 验证码
	sms = StringField(validators=[validators.DataRequired(message="请输入验证码")])

	def validate_username(self, value):
		u1 = BuyerUser.query.filter_by(username=value.data).first()
		if u1:
			raise validators.ValidationError('该用户名已经被注册了')

	def validate_tel(self, value):
		u1 = BuyerUser.query.filter_by(tel=value.data).first()
		if u1:
			raise validators.ValidationError('该电话号码已经被注册了')

	def validate_sms(self, value):
		api_redis = current_app.config.get('API_REDIS')
		raw_code = api_redis.get(self.tel.data)
		if not raw_code:
			raise validators.ValidationError('没有验证码，请点击发送验证码')
		if raw_code.decode('ascii') != value.data:
			raise validators.ValidationError('验证码不正确')


class BuyerAddressForm(Form):
	id = IntegerField(default=0)
	provence = StringField(validators=[validators.Length(max=16, message="不能超过8个字符")])
	# 市
	city = StringField(validators=[validators.Length(max=16, message="不能超过16个字符")])
	# 县
	area = StringField(validators=[validators.Length(max=16, message="不能超过16个字符")])
	# 详细地址
	detail_address = StringField(
		validators=[
			validators.DataRequired(message="请输入详细地址"),
			validators.Length(max=64, message="详细地址不能超过64个字符"),
		],
	)
	# 收货人姓名
	name = StringField(
		validators=[
			validators.DataRequired(message="请输入收货人姓名"),
			validators.Length(max=32, message="收货人姓名不能超过32个字符"),
		],
	)
	# 收货人电话
	tel = StringField(
		validators=[
			validators.DataRequired(message="请输入电话号码"),
			validators.Regexp(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18['
			                  r'0-9])|166|198|199)\d{8}$', message="请输入正确的电话号码"),
		],
	)

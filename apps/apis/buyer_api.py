from flask import request, jsonify, Flask, current_app, Response, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
from werkzeug.security import generate_password_hash, check_password_hash
from apps.apis import api_bp
from apps.forms.buyer_form import BuyerRegisterForm, BuyerAddressForm, BuyerLoginForm
from redis import Redis

from apps.models import BuyerUser, db, BuyerAddress
from apps.tools.token_tools import login_required


@api_bp.route('/sms/', endpoint='sms', methods=['GET'])
def get_sms():
	tel = request.args.get("tel")
	if tel:
		verify_code = "".join([str(random.choice(range(10))) for _ in range(4)])
		api_redis: Redis = current_app.config.get('API_REDIS')
		api_redis.set(tel, verify_code, current_app.config.get("SMS_LIFETIME"))
		# print(verify_code)
		return jsonify({'status': True, 'message': '成功发送验证码{}'.format(verify_code)})
	return jsonify({'status': False, 'message': '未有电话号码'})


# 买家用户注册api
@api_bp.route('/register/', endpoint='register', methods=['POST'])
def register():
	form = BuyerRegisterForm(request.form)
	print(form)
	if form.validate():
		buyer = BuyerUser()
		buyer.set_attr(form.data)
		db.session.add(buyer)
		db.session.commit()
		return jsonify({'status': "true", 'message': '注册成功'})
	else:
		return jsonify({
			'status': "false",
			'message': ' '.join(['{}:{}'.format(k, v[0]) for k, v in form.errors.items()])
		})


@api_bp.route('/login/', endpoint='login', methods=['POST'])
def buyer_login():
	loginform = BuyerLoginForm(request.form)

	if loginform.validate():
		name = loginform.data.get("name")
		user: BuyerUser = BuyerUser.query.filter_by(username=name).first()
		if user and check_password_hash(user.password, loginform.data.get("password")):
			data = Serializer(current_app.config.get("SECRET_KEY"), current_app.config.get("TOKEN_EXPIRES")).dumps(
				{"user_id": user.id})
			response: Response = jsonify(
				{"status": "true", "message": "登录成功", 'user_id': user.id, 'username': user.username})
			response.set_cookie('token', data.decode('ascii'))
			return response
		else:
			return jsonify({"status": "false", "message": "用户名或密码错误"})
	else:
		return jsonify({
			'status': "false",
			'message': ' '.join(['{}:{}'.format(k, v[0]) for k, v in loginform.errors.items()]),
		})


# 收获地址api
@api_bp.route('/address/', endpoint='address', methods=['GET'])
@login_required
def get_address_list():
	addresses = g.current_user.addresses
	addr_id = request.args.get('id')
	if addr_id:
		return jsonify(dict(addresses[int(addr_id) - 1]))
	result = [{**dict(address), 'id': num + 1} for num, address in enumerate(addresses)]

	return jsonify(result)


# 新增地址API
@api_bp.route('/address/', methods=['POST'])
@login_required
def add_address():
	address_form = BuyerAddressForm(request.form)
	message = "添加成功"
	if address_form.validate():
		if not address_form.id.data:
			# 说明是添加地址
			addr = BuyerAddress()
			addr.user = g.current_user
		else:
			# 说明是修改地址, id号以当前用户所管地址为序号规则
			addresses = g.current_user.addresses
			addr = addresses[address_form.id.data - 1]
			message = "更新成功"
		addr.set_attr(address_form.data)
		db.session.add(addr)
		db.session.commit()
		return jsonify({"status": "true", "message": message})
	return jsonify({"status": "false", "message": "添加失败"})



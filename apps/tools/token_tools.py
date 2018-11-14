from functools import wraps
from flask import request, current_app, g, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from apps.models import BuyerUser


def login_required(fun):
	@wraps(fun)
	def inner(*args, **kwargs):
		token = request.cookies.get("token")
		if not token:
			return jsonify({"status": "false", "message": "无效的token"})
		s = Serializer(current_app.config.get("SECRET_KEY"))
		data = s.loads(token)
		buyer = BuyerUser.query.filter_by(id=data.get("user_id")).first()
		if not buyer:
			return jsonify({"status": "false", "message": "无效的token"})
		g.current_user = buyer
		return fun(*args, **kwargs)

	return inner

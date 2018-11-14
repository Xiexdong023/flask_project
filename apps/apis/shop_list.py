import os
from flask import request

from apps.apis import api_bp
from flask import render_template

from apps.models import ShopModel
from flask import jsonify

from apps.models.shop_view import MenuCategory


@api_bp.route('/shop_list/', endpoint='shop_list', methods=['GET'])
def shop_list():
	stores = ShopModel.query.all()
	data = [{**dict(x), 'id': x.pub_id, } for x in stores]
	return jsonify(data)


@api_bp.route('/shop/', endpoint='shop', methods=['GET'])
def show_shop():
	shop_pid = request.args.get('id')
	shop = ShopModel.query.filter_by(pub_id=shop_pid).first()
	if not shop:
		return jsonify({'error': 'no shop'})

	cates = shop.categories

	commodity = [{
		**dict(cate),
		'goods_list': [{
			**dict(x),
			'goods_id': x.id,
		}
			for x in cate.goods]
	} for cate in cates]
	data = {**dict(shop), 'id': shop.pub_id, 'commodity': commodity, 'evaluate': []}
	return jsonify(data)

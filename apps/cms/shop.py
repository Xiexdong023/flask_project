from qiniu import Auth

from apps.cms import cms_bp
from flask import request, render_template, url_for, redirect, jsonify
from apps.models import db, ShopModel
from apps.forms.shop_form import ShopForm, CateForm, GoodsForm
from flask_login import current_user, login_required

from apps.models.shop_view import MenuCategory, GoodsModel
from apps.tools.my_func import generate_pub_id


@cms_bp.route("/add_shop/", endpoint="add_shop", methods=["GET", "POST"])
@login_required
def add_shop():
	form = ShopForm(request.form)
	if request.method == "POST" and form.validate():
		s1 = ShopModel()
		s1.set_attr(form.data)
		s1.pub_id = generate_pub_id()
		s1.seller = current_user
		db.session.add(s1)
		db.session.commit()
		return redirect(url_for("cms.index"))
	return render_template("add_shop.html", form=form, flags="添加店铺")


@cms_bp.route("/update_shop/<string:pub_id>/", endpoint="update_shop", methods=["GET", "POST"])
@login_required
def update_shop(pub_id):
	shop = ShopModel.query.filter_by(pub_id=pub_id).first()
	if not shop:
		return redirect(url_for("cms.index"))
	if request.method == "POST":
		form = ShopForm(request.form)
		if form.validate():
			shop.set_attr(form.data)
			db.session.commit()
			return redirect(url_for("cms.index", pub_id=pub_id))
	else:
		form = ShopForm(data=dict(shop))
	return render_template("add_shop.html", form=form, flags="店铺信息更新")


@cms_bp.route("/add_catgory/<string:pub_id>/", endpoint="add_catgory", methods=["GET", "POST"])
@login_required
def add_catgory(pub_id):
	form = CateForm(request.form)
	if request.method == "POST" and form.validate():
		shop = ShopModel.query.filter_by(pub_id=pub_id).first()
		if shop:  # 一般情况shop部位None,防止人为改动浏览器url参数
			if form.is_default.data:
				for cate in shop.categories:
					cate.is_default = False
			cate = MenuCategory()
			cate.set_attr(form.data)
			cate.shop_pid = shop.pub_id
			db.session.add(cate)
			db.session.commit()
			return redirect(url_for("cms.index"))
	return render_template("shop_catgory.html", flags="添加菜品分类", form=form)


@cms_bp.route("/check_catgory/<string:pub_id>/", endpoint="check_catgory", methods=["GET", "POST"])
@login_required
def check_catgory(pub_id):
	shop = ShopModel.query.filter_by(pub_id=pub_id).first()
	return render_template("shop_check_catgory.html", shop=shop)


"""http://47.104.204.72:9002/cms/ 老师部署项目"""


@cms_bp.route("/add_goods/<pub_id>/", endpoint="add_goods", methods=["GET", "POST"])
def add_goods(pub_id):
	form = GoodsForm(pub_id, request.form)
	if request.method == "POST":
		if form.validate():
			good = GoodsModel()
			good.set_attr(form.data)
			db.session.add(good)
			db.session.commit()
			return redirect(url_for("cms.index"))
	return render_template("add_goods.html", form=form, flags="菜品添加")


@cms_bp.route("/show_goods/<string:pub_id>/", endpoint="show_goods", methods=["GET"])
def show_goods(pub_id):
	shop = ShopModel.query.filter_by(pub_id=pub_id).first()
	return render_template("show_goods.html", flags="菜品查看", shop=shop)


@cms_bp.route("/update_goods/<pub_id>/<good_id>/", endpoint="update_goods", methods=["GET", "POST"])
def update_goods(pub_id, good_id):
	good = GoodsModel.query.filter_by(id=good_id).first()
	if request.method == "POST":
		form = GoodsForm(pub_id, request.form)
		if form.validate():
			good.set_attr(form.data)
			db.session.commit()
			return redirect(url_for("cms.index"))
	else:
		form = GoodsForm(pub_id, data=dict(good))
	return render_template("update_goods.html", form=form, flags="菜品信息更新")


@cms_bp.route("/uptoken/", methods=["GET", "POST"])
def get_token():
	access_key = 'S9TrdZka2Yf59m5-Td4Oo6GU9keUyXdIKTL0lwfZ'
	secret_key = 'HmIorycKuCc_ypBIePM6RkmrnyQdBVRM6ueC5jfk'

	q = Auth(access_key=access_key, secret_key=secret_key)
	token = q.upload_token('eleme')
	return jsonify({"uptoken": token})

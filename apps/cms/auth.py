from flask import render_template, url_for, redirect, request, make_response
from werkzeug.wrappers import Response
from flask_login import login_user, logout_user, login_required
from apps.cms import cms_bp
from apps.forms.sellerform import SellerLoginForm, SellerRegisterForm
from apps.models import CmsSellerModel, db
from flask import session


@cms_bp.route("/", endpoint="index")
def index():
	return render_template("index.html")


@cms_bp.route("/register/", endpoint="register", methods=["GET", "POST"])
def register():
	form = SellerRegisterForm(request.form)

	if request.method == "POST" and form.validate():
		seller = CmsSellerModel()
		seller.set_attr(form.data)
		db.session.add(seller)
		db.session.commit()
		return redirect(url_for("cms.index"))
	return render_template("login_register.html", form=form, flags="注册")


@cms_bp.route("/login/", endpoint="login", methods=["GET", "POST"])
def login():
	form = SellerLoginForm(request.form)
	if request.method == "POST" and form.validate():
		seller = CmsSellerModel.query.filter_by(username=form.username.data).first()
		if seller and seller.check_password(form.password.data):
			login_user(seller)
			return redirect(url_for('cms.index'))
		form.password.errors = ["用户名或密码错误"]
	return render_template("login_register.html", form=form, flags="登录")


@cms_bp.route("/logout/", endpoint="logout")
@login_required
def logout():
	logout_user()
	response = redirect(url_for("cms.index"))
	return response

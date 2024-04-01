from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('成功登录', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('密码无效', category='error')
        else:
            flash('邮箱不存在', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('邮箱已经纯在', category='error')
        elif len(email) < 4:
            flash('邮箱要有3个特征.', category='error')
        elif len(first_name) < 2:
            flash('名字要大于1', category='error')
        elif password1 != password2:
            flash('密码匹配错误', category='error')
        elif len(password1) < 7:
            flash('密码至少要有7位数', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('账户成功创建', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

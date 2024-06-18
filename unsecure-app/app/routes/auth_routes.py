from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.services import user_service
from app.models.user import User
from app.forms.register_form import RegistrationForm
from app.forms.login_form import LoginForm

from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            birth_date=form.birth_date.data
        )

        user_service.add_user(user);
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_service.get_user_by_email(form.email.data)
        if user:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Wrong email or password', 'error')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


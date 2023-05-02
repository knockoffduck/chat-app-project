from flask import Blueprint, render_template, flash, redirect, url_for, request
from website.models import User
from website import db
from website.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

auth = Blueprint("auth", __name__)

# @auth.route("/login")
# def login():
#     return render_template("login.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('views.chat_route')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# @auth.route("/logout")
# def logout():
#     return "<h1>Logout</h1>"

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


# @auth.route("/signup")
# def signup():
#     return "<h1>SignUp</h1>"

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('sign_up.html', title='Sign Uppy', form=form)

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users, db
from .config import Config
from flask_login import login_user, logout_user, login_required
import datetime, jwt

auth = Blueprint('auth', __name__)
uid = ''

def encode_auth_token():
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=45),
            'iat': datetime.datetime.utcnow(),
            'sub': session['_user_id']
        }
        return jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        with open('exc.txt', 'w') as file:
            file.write(str(e))
        return "Fail"

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = Users.query.filter_by(email=email).first()
    if user:
        return redirect(url_for('auth.signup'))

    new_user = Users(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    token = encode_auth_token().decode('UTF-8')
    session['token'] = token
    if user:
        flash('Email address already exists')

    return redirect(url_for('main.profile'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    token = encode_auth_token()
    try:
        token = token.decode('UTF-8')
    except:
        pass
    session['token'] = token

    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



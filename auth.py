from flask import Blueprint, request, jsonify, render_template, redirect, url_for

from flask_login import login_user, logout_user, current_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from prometheus_client import start_http_server, Counter, Gauge

from app.models import db, User

auth = Blueprint('auth', __name__)

BAD_ADMIN_ACCESS_COUNTER = Counter('bad_admin_requests_total','Number of Bad Admin Access requests')

number_users = Gauge('number_users', 'Number of users')

@auth.route('/register', methods=['POST'])

def register():

    data = request.get_json()
    
    # check if email is already in use and throw error if it is
    duplicate_check = User.query.filter_by(email=data['email']).first()
    if duplicate_check:
        return jsonify({'error': 'Email already registered'}), 401

    user = User(

        email=data['email'],

        password_hash=generate_password_hash(data['password'])

    )
    # check that @ symbol is in email
    if "@" in user.email:

       db.session.add(user)

       db.session.commit()

       return jsonify({'message': 'User created'}), 201

    else:
        
       return jsonify({'error': 'Invalid email'}), 401

@auth.route('/login', methods=['POST'])

def login():

    number_users.inc()

    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password_hash, data['password']):

        login_user(user)

        return jsonify({'message': 'Logged in'})

    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/logout')

def logout():

    number_users.dec()
    
    logout_user()

    return jsonify({'message': 'Logged out'})

# allow admin to access admin.html and redirect non-admin

@auth.route('/admin')

@login_required

def admin():

    user = User.query.filter_by(email=current_user.email).first()

    if user and user.is_admin:
    
        return render_template('admin.html')
    
    else:

        BAD_ADMIN_ACCESS_COUNTER.inc()

        print("Bad Admin Access Attempts: " + str(BAD_ADMIN_ACCESS_COUNTER._value.get()))

        return render_template('not_admin.html')

from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer as usts
from threading import Thread
from datetime import datetime

from app import app, db, mail
from app.models import User
from .forms import EmailForm, LoginForm, PasswordForm, RegisterForm

# config

users_blueprint=Blueprint('users', __name__)

# helper functions

# execute send_email function asynchronously

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

# send_mail

def send_email(subject, recipients, html_body):
    msg=Message(subject, recipients=recipients)
    msg.html=html_body
    thr=Thread(target=send_async_email, args=[msg])
    thr.start()

# confirm email

def send_confirmation_email(user_email):
    confirm_serializer=usts(app.config['SECRET_KEY'])

    confirm_url=url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True
        )

    html=render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)

    send_email('Confirm Your Email Address', [user_email], html)

# reset email

def send_password_reset_email(user_email):
    password_reset_serializer=usts(app.config['SECRET_KEY'])

    password_reset_url=url_for(
        'users.reset_with_token',
        token=password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)

    html=render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)

    send_email('Password Reset Requested', [user_email], html)    

# routes

# register

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm(request.form)
    if request.method=='POST':
        if form.validate_on_submit():
            try:
                new_user=User(form.email.data, form.password.data)
                new_user.authenticated=True
                db.session.add(new_user)
                db.session.commit()
                
                # Eliminate logging in immediately after registration
                login_user(new_user)
                
                send_confirmation_email(new_user.email)
                flash('Thank you for registering! Please check your email to confirm your email address.', 'success')
                return redirect(url_for('recipes.index'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('register.html', form=form)

# confirm email

@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer=usts(app.config['SECRET_KEY'])
        email=confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    user=User.query.filter_by(email=email).first()

    if user.email_confirmed:
        flash('Account already confirmed. Please log in.', 'info')
    else:
        user.email_confirmed=True
        user.email_confirmed_on=datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Thank you for confirming your email address!', 'info')

    return redirect(url_for('recipes.index'))

# login

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm(request.form)
    if request.method=='POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated=True
                
                # Indicate current user and when they last logged in
                user.last_logged_in=user.current_logged_in
                user.current_logged_in=datetime.now()
                
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thank you for logging in, {}!'.format(current_user.email), 'success')
                return redirect(url_for('recipes.index'))
            else:
                flash('Incorrect log-in credentials!', 'error') 
    return render_template('login.html', form=form)

# logout

@users_blueprint.route('/logout')
@login_required
def logout():
    user=current_user
    user.authenticated=False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('users.login'))

# reset password

@users_blueprint.route('/reset', methods=['GET', 'POST'])
def reset():
    form=EmailForm()
    if form.validate_on_submit():
        try:
            user=User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Invalid email address', 'error')
            return render_template('password_reset_email.html', form=form)

        if user.email_confirmed:
            send_password_reset_email(user.email)
            flash('Please check your email for the password reset link.', 'success')
        else:
            flash('Your email address must be confirmed before attempting a password reset.', 'error')
        return redirect(url_for('users.login'))

    return render_template('password_reset_email.html', form=form)


@users_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        password_reset_serializer=usts(app.config['SECRET_KEY'])
        email=password_reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    form=PasswordForm()

    if form.validate_on_submit():
        try:
            user=User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address', 'error')
            return redirect(url_for('users.login'))

        user.password=form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')

        return redirect(url_for('users.login'))

    return render_template('reset_password_with_token.html', form=form, token=token)

# user profile

@users_blueprint.route('/user_profile')
@login_required
def user_profile():
    return render_template('user_profile.html')

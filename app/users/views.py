from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
from sqlalchemy.exc import IntegrityError

from app import db, mail
from app.models import User
from forms import LoginForm, RegisterForm

# config

users_blueprint=Blueprint('users', __name__)

# mail sending helper function

def send_email(subject, recipients, text_body, html_body):
    msg=Message(subject, recipients=recipients)
    msg.body=text_body
    msg.html=html_body
    mail.send(msg)

# routes

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

                send_email('Marundu Recipe App Registration Confirmation',
                            ['marundu@gmail.com'],
                            'Thank you for registering with the Marundu Recipe App!',
                            '<h3>Thank you for registering with the Marundu Recipe App!</h3>'
                    )

                flash('Thank you for registering!', 'success')
                return redirect(url_for('recipes.index'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('register.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm(request.form)
    if request.method=='POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated=True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thank you for logging in, {}!'.format(current_user.email), 'success')
                return redirect(url_for('recipes.index'))
            else:
                flash('Incorrect log-in credentials!', 'error') 
    return render_template('login.html', form=form)

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

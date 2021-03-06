from flask import Blueprint, current_app, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from iwbt import get_session
from iwbt.blueprints.social.forms import LoginForm, SignUpForm
from iwbt.models.social import *


social = Blueprint('social', __name__, url_prefix='user')


@social.route('/<user>')
def user_page(user):
    session = get_session(current_app)
    user = session.query(User).filter(User.alias == user).first()
    return render_template('social/user.html', user=user)


@social.route('/login', methods=['GET', 'POST'])
def login():
    session = get_session(current_app)
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = session.query(User).filter(User.alias == login_form.alias.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            flash('You have successfully logged in to account %s' % user.alias, 'alert alert-success')
            login_user(user)
            return redirect(request.args.get('next') or url_for('social.user_page', user=user.alias))
        else:
            flash('UserName or Password Incorrect. Go Away :(', 'alert alert-danger')
        session.close()
        return redirect(url_for('social.login'))
    return render_template('social/login.html', form=login_form)


@social.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'alert alert-danger')
    return redirect(url_for('river', name='Chattooga'))


@social.route('/signup', methods=['GET', 'POST'])
def sign_up():
    session = get_session(current_app)
    suf = SignUpForm()

    if suf.validate_on_submit():
        user = session.query(User).filter(or_(User.alias == suf.alias.data, User.email == suf.email.data)).first()
        if user:
            flash('User Name or Email already taken', 'alert alert-danger')
            return redirect("{{ url_for(social.sign_up) }}")
        flash('You have successfully signed up for an account with username %s' % suf.alias.data, 'alert alert-success')
        user = User(alias=suf.alias.data,
                    first_name=suf.first_name.data,
                    last_name=suf.last_name.data,
                    email=suf.email.data,
                    password=suf.password.data)
        session.add(user)
        session.commit()
        return redirect(url_for('social.login'))
    return render_template('social/signup.html', form=suf)


@social.route('/<alias>/log')
def paddle_log(alias):
    session = get_session(current_app)
    u = session.query(User).filter(User.alias == alias).first()
    return render_template('social/paddlelog.html', user=u)
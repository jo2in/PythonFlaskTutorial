# Copyright
# Brief description
import logging
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from helloworld import app, db
from helloworld.models import User, Course
from helloworld.forms import LoginForm, RegistrationForm


@app.route('/')
@app.route('/index')
def index():
    courses = [
        {'title': 'Course1', 'description': 'some fancy stuff'},
        {'title': 'Course1', 'description': 'some other fancy stuff'}
    ]
    return render_template('index.html', title='Home', courses=courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        if not url_parse(next_page).netloc:
            logging.warning('URL: "{}"'.format(url_parse(next_page).netloc))
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/courses', methods=['GET'])
@login_required
def courses():
    courses = [
        {'title': 'Course1', 'description': 'some fancy stuff'},
        {'title': 'Course1', 'description': 'some other fancy stuff'}
    ]
    return render_template('courses.html', title='Courses', courses=courses)


@app.route('/user/<username>')
@login_required
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    subscribed_courses = user.courses.paginate(page, 20, False)
    next_url, prev_url = None, None

    if subscribed_courses.has_next:
        next_url = url_for('/user/{}'.format(username), page=subscribed_courses.next_num)

    if subscribed_courses.has_prev:
        prev_url = url_for('/user/{}'.format(username), page=subscribed_courses.prev_num)

    return render_template('user.html',
                           subscribed_courses=subscribed_courses.items,
                           page=page,
                           next_url=next_url,
                           prev_url=prev_url)


@app.before_request
def update_last_visit():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

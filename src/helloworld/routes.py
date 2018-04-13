# Copyright
# Brief description
from flask import render_template, flash, redirect, url_for
from helloworld import app
from helloworld.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jozef'}
    courses = [
        {'title': 'Course1', 'description': 'some fancy stuff'},
        {'title': 'Course1', 'description': 'some other fancy stuff'}
    ]
    return render_template('index.html', title='Home', user=user, courses=courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

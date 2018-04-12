# Copyright
# Brief description
from flask import render_template
from helloworld import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jozef'}
    courses = [
        {'title': 'Course1', 'description': 'some fancy stuff'},
        {'title': 'Course1', 'description': 'some other fancy stuff'}
    ]
    return render_template('index.html', title='Home', user=user, courses=courses)

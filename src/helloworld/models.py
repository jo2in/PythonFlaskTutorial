import jwt
from datetime import datetime, timedelta

from hashlib import md5


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from helloworld import app, db
from helloworld import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


subscriptions = db.Table('subscriptions',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                         db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                         )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    courses = db.relationship('Course', secondary=subscriptions,
                              backref=db.backref('course_participant', lazy=True), lazy='dynamic')

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.now() + timedelta(seconds=expires_in)},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except jwt.JWTError as e:
            app.logger.error('Decoding error: {}'.format(e))
            return

        return User.query.get(id)

    def avatar(self, size=128):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def subscribe(self, course):
        self.courses.append(course)

    def unsubscribe(self, course):
        self.courses.remove(course)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(140), index=True)
    subscribers = db.relationship('User', secondary=subscriptions,
                                  backref=db.backref('subscribed_courses', lazy=True), lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.title)

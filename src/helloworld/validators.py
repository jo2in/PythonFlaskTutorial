from wtforms.validators import ValidationError

from helloworld.models import User


class DataUnique(object):
    def __init__(self, message="Provided data is not unique"):
        self.message = message

    def __call__(self, form, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(self.message)

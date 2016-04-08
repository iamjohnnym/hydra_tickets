from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, NumberRange, Regexp


class LoginForm(Form):
    sso = TextField(
            'SSO',
            [Required('SSO must be supplied')]
            )
    password = PasswordField(
            'Password',
            [Required("Password must be entered")]
            )
    remember_me = BooleanField(
            'remember_me',
            default=False
            )

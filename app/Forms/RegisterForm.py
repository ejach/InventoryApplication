from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    confPass = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit', id='registerBtn')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TelField
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
    phone = TelField(
        'Phone Number',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit', id='registerBtn')

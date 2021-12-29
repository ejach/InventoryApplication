from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class VanForm(FlaskForm):
    van_number = StringField(
        'Van Number',
        validators=[DataRequired()]
    )
    btnSubmit = SubmitField('Add Van')

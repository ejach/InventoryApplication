from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class LowPartsForm(FlaskForm):
    user = SelectField(
        'Select User',
        validators=[DataRequired()]
    )
    submitBtn = SubmitField('Submit')

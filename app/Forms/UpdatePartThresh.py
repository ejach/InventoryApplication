from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class UpdatePartThresh(FlaskForm):
    id = HiddenField()
    newThresh = IntegerField(
        'Threshold',
        validators=[DataRequired()]
    )
    submitBtn = SubmitField('Submit')

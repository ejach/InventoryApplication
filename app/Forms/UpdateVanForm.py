from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class UpdateVanForm(FlaskForm):
    id = HiddenField()
    vanNumber = StringField(
        'Van Number',
        validators=[DataRequired()]
    )
    confirmUpdateBtn = SubmitField('Submit')

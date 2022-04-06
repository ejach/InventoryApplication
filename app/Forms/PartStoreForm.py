from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PartStoreForm(FlaskForm):
    partStoreName = StringField(
        'Part Store Name',
        validators=[DataRequired()]
    )
    btnSubmit = SubmitField('Add Part Store')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class PartStoreForm(FlaskForm):
    partStoreName = StringField(
        'Part Store Name',
        validators=[DataRequired()]
    )
    partStoreImage = SelectField(
        'Select Part Store Image',
        validators=[DataRequired()]
    )
    btnSubmit = SubmitField('Add Part Store')

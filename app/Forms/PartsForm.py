from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class PartsForm(FlaskForm):
    partName = StringField(
        'Part Name',
        validators=[DataRequired()]
    )
    partNumber = StringField(
        'Part Number',
        validators=[DataRequired()]
    )
    partAmount = IntegerField(
        'Part Amount',
        validators=[DataRequired()]
    )
    partStore = SelectField(
        'Select Part Store',
        validators=[DataRequired()]
    )

    unit = SelectField(
        'Select Unit',
        validators=[DataRequired()]
    )

    submit = SubmitField('Submit', id='submit')

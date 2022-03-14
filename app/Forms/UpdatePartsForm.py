from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired


class UpdatePartsForm(FlaskForm):
    id = HiddenField()
    partName = StringField(
        'Part Name',
        validators=[DataRequired()]
    )
    partNumber = StringField(
        'Part Number',
        validators=[DataRequired()]
    )
    newPartAmount = IntegerField(
        'Part Amount',
        validators=[DataRequired()]
    )
    newVan = SelectField(
        validators=[DataRequired()]
    )
    newUnit = SelectField(
        'Select Unit',
        validators=[DataRequired()]
    )
    confirmUpdateBtn = SubmitField('Submit')

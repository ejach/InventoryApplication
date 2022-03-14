from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddTypeForm(FlaskForm):
    typeName = StringField(
        'Type Name',
        validators=[DataRequired()]
    )
    typeUnit = StringField(
        'Type Unit',
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

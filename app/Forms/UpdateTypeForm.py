from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class UpdateTypeForm(FlaskForm):
    id = HiddenField()

    newTypeName = StringField(
        'Type Name',
        validators=[DataRequired()]
    )
    newTypeUnit = StringField(
        'Type Unit',
        validators=[DataRequired()]
    )
    confirmUpdateBtn = SubmitField('Submit')

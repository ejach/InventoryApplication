from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class UpdatePartStoreForm(FlaskForm):
    id = HiddenField()
    partStoreName = StringField(
        'Part Store Name',
        validators=[DataRequired()]
    )
    newPartStoreImage = SelectField(
        'Select Part Store Image',
        validators=[DataRequired()]
    )
    confirmUpdateBtn = SubmitField('Submit')

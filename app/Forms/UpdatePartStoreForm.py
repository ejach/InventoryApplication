from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class UpdatePartStoreForm(FlaskForm):
    id = HiddenField()
    partStoreName = StringField(
        'Part Store Name',
        validators=[DataRequired()]
    )
    confirmUpdateBtn = SubmitField('Submit')

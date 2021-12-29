from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired
from app.Database.DatabaseManipulator import DatabaseManipulator


def get_selections():
    dbm = DatabaseManipulator()
    results = dbm.get_van_nums()
    return results


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
        validators=[DataRequired()],
        choices=[(g[1], g[1]) for g in get_selections()]
    )
    confirmUpdateBtn = SubmitField('Submit')

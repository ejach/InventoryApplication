from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from app.Database.DatabaseManipulator import DatabaseManipulator


def get_selections():
    dbm = DatabaseManipulator()
    results = dbm.get_van_nums()
    return results


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
    van = SelectField(
        'Select Van',
        validators=[DataRequired()],
        choices=[(g[1], g[1]) for g in get_selections()]
    )
    submit = SubmitField('Submit', id='submit')

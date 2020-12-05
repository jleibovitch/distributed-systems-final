from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

class TapForm(FlaskForm):
    account_no = StringField('Account Number', validators=[DataRequired()])
    tap_btn = SubmitField('Scan card/device here!')
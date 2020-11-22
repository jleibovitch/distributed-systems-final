from flask_wtf import FlaskForm
from wtforms import SubmitField

class Btn(FlaskForm):
    tap = SubmitField('Scan card/device here!')
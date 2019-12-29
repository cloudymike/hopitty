from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CmdForm(FlaskForm):
    username = StringField('Command', validators=[DataRequired()])
    submit = SubmitField('Execute')
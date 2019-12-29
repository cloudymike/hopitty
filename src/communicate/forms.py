from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CmdForm(FlaskForm):
    command = StringField('Command', validators=[DataRequired()])
    submit = SubmitField('Execute')
    
class LoadForm(FlaskForm):
    load = StringField('Stages json', validators=[DataRequired()])
    submit = SubmitField('Execute')
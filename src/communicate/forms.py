from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired

class CmdForm(FlaskForm):

    #command = StringField('Command', validators=[DataRequired()])
    command = RadioField('Command', choices=[('stop','stop'),('run','run'),('pause','pause'),('skip','skip'),('terminate','terminate')])
    submit = SubmitField('Execute')
    
class LoadForm(FlaskForm):
    load = StringField('Stages json', validators=[DataRequired()])
    submit = SubmitField('Execute')
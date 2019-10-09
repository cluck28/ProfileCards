
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AnswerForm(Form):
    '''
    Allow users to answer a question
    '''
    answer = TextAreaField('Answer', validators=[DataRequired()])

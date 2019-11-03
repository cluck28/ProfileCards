
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

difficulty_choices = [('1','1 (Easy)'),('2','2'),('3','3 (Moderate)'),('4','4'),('5','5 (Hard)')]

class AnswerForm(Form):
    '''
    Allow users to answer a question
    '''
    answer = TextAreaField('Answer', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=difficulty_choices, validators=[DataRequired()])


from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

category_choices = [('Machine Learning','Machine Learning'),('Computer Science','Computer Science'),
                    ('Statistics','Statistics'),('Combinatorics','Combinatorics'),('Case Study','Case Study'),
                    ('Systems Design','Systems Design'),('Behavioral','Behavioral')]

class QuestionForm(Form):
    '''
    Allow users to input a question and question category
    '''
    category = SelectField('Category', choices=category_choices, validators=[DataRequired()])
    question = TextAreaField('Question', validators=[DataRequired()])

from flask_wtf import Form
from flask import request
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

category_choices = [('Machine Learning','Machine Learning'),('Computer Science','Computer Science'),
                    ('Statistics','Statistics'),('Combinatorics','Combinatorics'),('Case Study','Case Study'),
                    ('Systems Design','Systems Design'),('Behavioral','Behavioral')]

difficulty_choices = [('1','1 (Easy)'),('2','2'),('3','3 (Moderate)'),('4','4'),('5','5 (Hard)')]

class QuestionForm(Form):
    '''
    Allow users to input a question and question category
    '''
    category = SelectField('Category', choices=category_choices, validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=difficulty_choices, validators=[DataRequired()])
    question = TextAreaField('Question', validators=[DataRequired()])

class AnswerForm(Form):
    '''
    Allow users to answer a question
    '''
    answer = TextAreaField('Answer', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=difficulty_choices, validators=[DataRequired()])

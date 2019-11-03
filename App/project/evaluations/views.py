# project/evaluations/views.py
"""
Created on Sat Oct 5, 2019

@author: christopherluciuk
"""

from flask import render_template, Blueprint, request, redirect, url_for, flash, json, g
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.sql import func, desc
from sqlalchemy.sql.expression import cast
import sqlalchemy
from sqlalchemy.sql.functions import coalesce
import sys

from project import db, mail, app
from .forms import QuestionForm, AnswerForm
from project.models import Evaluation, Answer, Evaluation_Likes, Evaluation_Difficulty

evaluations_blueprint = Blueprint('evaluations', __name__)

@evaluations_blueprint.route('/')
@evaluations_blueprint.route('/index')
def index():
    '''
    Render the landing page
    '''
    return render_template("index.html")

@evaluations_blueprint.route('/add_question', methods=['GET','POST'])
@login_required
def add_question():
    form = QuestionForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_question = Evaluation(form.category.data,form.question.data,current_user.id)
            db.session.add(new_question)
            db.session.flush()
            new_rating = Evaluation_Difficulty(current_user.id,new_question.id,form.difficulty.data)
            db.session.add(new_rating)
            db.session.commit()
            return redirect(url_for('evaluations.question_view'))
    return render_template("add_question.html",form=form)

@evaluations_blueprint.route('/question_view', methods=['GET','POST'])
@login_required
def question_view():
    #Categories for filters
    categories = ['Machine Learning','Computer Science','Statistics','Combinatorics','Case Study',\
                        'Systems Design','Behavioral']
    if request.method == 'POST':
        print(request.form.getlist('category'))
        category = request.form.getlist('category')
        filter_questions_likes = db.session.query(Evaluation.id,Evaluation.evaluation_category,\
                            Evaluation.evaluation_question,cast(coalesce(func.avg(Evaluation_Likes.like),0),sqlalchemy.Integer).\
                            label('Likes'),cast(coalesce(func.avg(Evaluation_Difficulty.difficulty),0),sqlalchemy.Integer).label('Difficulty')).\
                            outerjoin(Evaluation_Likes).outerjoin(Evaluation_Difficulty).group_by(Evaluation.id).\
                            filter(Evaluation.evaluation_category.in_(category)).order_by(desc('Likes')).all()
        return render_template('question_view.html', questions_likes=filter_questions_likes, categories=categories)
    #Count likes for each question
    questions_likes = db.session.query(Evaluation.id,Evaluation.evaluation_category,\
                    Evaluation.evaluation_question,cast(coalesce(func.avg(Evaluation_Likes.like),0),sqlalchemy.Integer).\
                    label('Likes'),cast(coalesce(func.avg(Evaluation_Difficulty.difficulty),0),sqlalchemy.Integer).label('Difficulty')).\
                    outerjoin(Evaluation_Likes).outerjoin(Evaluation_Difficulty).group_by(Evaluation.id).order_by(desc('Likes')).all()
    return render_template('question_view.html', questions_likes=questions_likes, categories=categories)

@evaluations_blueprint.route('/user_question_view')
@login_required
def user_question_view():
    questions_likes = db.session.query(Evaluation.id,Evaluation.evaluation_category,\
                    Evaluation.evaluation_question,cast(coalesce(func.avg(Evaluation_Likes.like),0),sqlalchemy.Integer).\
                    label('Likes'),cast(coalesce(func.avg(Evaluation_Difficulty.difficulty),0),sqlalchemy.Integer).label('Difficulty')).\
                    outerjoin(Evaluation_Likes).outerjoin(Evaluation_Difficulty).group_by(Evaluation.id).\
                    filter(Evaluation.user_id == current_user.id).order_by(desc('Likes')).all()
    return render_template('user_question_view.html', questions_likes=questions_likes)

@evaluations_blueprint.route('/add_evaluation_like', methods=['POST'])
@login_required
def add_evaluation_like():
    if request.method == 'POST':
        question_id = request.form['question_id']
        #Get all the likes for this question
        evaluation_likes = Evaluation_Likes.query.filter(Evaluation_Likes.evaluation_id==question_id)
        #Has the current user liked the question?
        if evaluation_likes.filter(Evaluation_Likes.user_id == current_user.id).first() is not None:
            #Unlike the question
            db.session.delete(evaluation_likes.filter(Evaluation_Likes.user_id == current_user.id).first())
            db.session.commit()
            message = 'You disliked this'
        #If not, like the question
        else:
            #Like the question
            db.session.add(Evaluation_Likes(current_user.id, question_id, 1))
            db.session.commit()
            message = 'You liked this'
    ctx = {'likes_count': evaluation_likes.count(), 'message': message}
    response = app.response_class(response=json.dumps(ctx), status=200, mimetype='application/json')
    return response

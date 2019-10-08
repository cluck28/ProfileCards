# project/evaluations/views.py
"""
Created on Sat Oct 5, 2019

@author: christopherluciuk
"""

from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user

from project import db, mail, app
from .forms import QuestionForm, AnswerForm
from project.models import Evaluation, Answer

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
            new_question = Evaluation(form.category.data,form.question.data)
            db.session.add(new_question)
            db.session.commit()
            flash('Question successfully uploaded.', 'success')
            return redirect(url_for('evaluations.index'))
    return render_template("add_question.html",form=form)

@evaluations_blueprint.route('/question_view')
@login_required
def question_view():
    questions = Evaluation.query.order_by(Evaluation.id).all()
    return render_template('question_view.html', questions=questions)

@evaluations_blueprint.route('/answer_question/<question_id>', methods=['GET','POST'])
def answer_question(question_id):
    question = db.session.query(Evaluation).filter(Evaluation.id == question_id).first()
    form = AnswerForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_answer = Answer(form.answer.data)
            db.session.add(new_answer)
            db.session.commit()
            flash('Question successfully answered', 'success')
            return redirect(url_for('evaluations.question_view'))
    return render_template("answer_question.html",form=form,question=question)

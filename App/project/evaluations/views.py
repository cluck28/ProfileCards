# project/evaluations/views.py
"""
Created on Sat Oct 5, 2019

@author: christopherluciuk
"""

from flask import render_template, Blueprint, request, redirect, url_for, flash

from project import db, mail, app
from .forms import QuestionForm
from project.models import Evaluation

evaluations_blueprint = Blueprint('evaluations', __name__)

@evaluations_blueprint.route('/')
@evaluations_blueprint.route('/index')
def index():
    '''
    Render the landing page
    '''
    return render_template("index.html")

@evaluations_blueprint.route('/add_question', methods=['GET','POST'])
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


from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user

from project import db, mail, app
from .forms import AnswerForm
from project.models import Evaluation, Answer

answers_blueprint = Blueprint('answers', __name__)

@answers_blueprint.route('/view_answers/<question_id>',methods=['GET','POST'])
@login_required
def view_answers(question_id):
    question = db.session.query(Evaluation).filter(Evaluation.id == question_id).first()
    answers = db.session.query(Answer).filter(Answer.evaluation_id == question_id).all()
    return render_template("answer_view.html",question=question,answers=answers)

@answers_blueprint.route('/answer_question/<question_id>', methods=['GET','POST'])
@login_required
def answer_question(question_id):
    #Check if user has answered the question
    if db.session.query(Answer).filter(Answer.evaluation_id == question_id).\
    filter(Answer.user_id == current_user.id).first() is not None:
        flash('Question already answered', 'success')
        return redirect(url_for('answers.view_answers',question_id=question_id))
    else:
        question = db.session.query(Evaluation).filter(Evaluation.id == question_id).first()
        form = AnswerForm(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                new_answer = Answer(form.answer.data,current_user.id,question_id)
                db.session.add(new_answer)
                db.session.commit()
                flash('Question successfully answered', 'success')
                return redirect(url_for('answers.view_answers',question_id=question_id))
        return render_template("answer_question.html",form=form,question=question)

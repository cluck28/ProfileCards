
from flask import render_template, Blueprint, request, redirect, url_for, flash, json
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy.sql import func, desc

from project import db, mail, app
from .forms import AnswerForm
from project.models import Evaluation, Answer, Answer_Vote, Evaluation_Difficulty

answers_blueprint = Blueprint('answers', __name__)

@answers_blueprint.route('/view_answers/<question_id>',methods=['GET','POST'])
@login_required
def view_answers(question_id):
    question = db.session.query(Evaluation).filter(Evaluation.id == question_id).first()
    #Need to include the upvotes here
    answers = db.session.query(Answer).filter(Answer.evaluation_id == question_id).all()
    answers_upvotes = db.session.query(Answer.id,Answer.answer_content,\
                        func.count(Answer_Vote.vote).label('Upvotes')).\
                        outerjoin(Answer_Vote).filter(Answer.evaluation_id == question_id).\
                        group_by(Answer.id).order_by(desc('Upvotes')).all()
    return render_template("answer_view.html",question=question,answers_upvotes=answers_upvotes)

@answers_blueprint.route('/answer_question/<question_id>', methods=['GET','POST'])
@login_required
def answer_question(question_id):
    question = db.session.query(Evaluation).filter(Evaluation.id == question_id).first()
    form = AnswerForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_answer = Answer(form.answer.data,current_user.id,question_id)
            db.session.add(new_answer)
            new_rating = Evaluation_Difficulty(current_user.id,question_id,form.difficulty.data)
            db.session.add(new_rating)
            db.session.commit()
        return redirect(url_for('answers.view_answers',question_id=question_id))
    return render_template("answer_question.html",form=form,question=question)


@answers_blueprint.route('/has_user_answered', methods=['GET','POST'])
@login_required
def has_user_answered():
    #Check if user has answered the question
    if request.method == 'POST':
        question_id = request.form['question_id']
        if db.session.query(Answer).filter(Answer.evaluation_id == question_id).\
                                    filter(Answer.user_id == current_user.id).first() is not None:
            message = 'Question already answered'
            answer_status = 1
        else:
            message = 'Submit answer to view all solutions.'
            answer_status = 0
    ctx = {'message': message,'status': answer_status, 'url': url_for('answers.view_answers',question_id=question_id)}
    response = app.response_class(response=json.dumps(ctx), status=200, mimetype='application/json')
    return response

@answers_blueprint.route('/add_answer_upvote', methods=['POST'])
@login_required
def add_answer_upvote():
    if request.method == 'POST':
        answer_id = request.form['answer_id']
        #Get all the likes for this question
        answer_upvotes = Answer_Vote.query.filter(Answer_Vote.answer_id==answer_id)
        #Add an upvote
        db.session.add(Answer_Vote(current_user.id, answer_id, 1))
        db.session.commit()
        message = 'You added an upvote'

    ctx = {'upvotes_count': answer_upvotes.count(), 'message': message}
    response = app.response_class(response=json.dumps(ctx), status=200, mimetype='application/json')
    return response

@answers_blueprint.route('/user_answer_view',methods=['GET','POST'])
@login_required
def user_answer_view():
    answers_upvotes = db.session.query(Answer.id,Answer.answer_content,\
                        func.count(Answer_Vote.vote).label('Upvotes')).\
                        outerjoin(Answer_Vote).filter(Answer.user_id == current_user.id).\
                        group_by(Answer.id).order_by(desc('Upvotes')).all()
    return render_template("user_answer_view.html",answers_upvotes=answers_upvotes)

# project/users/views.py
"""
Created on Sat Oct 5, 2019

@author: christopherluciuk
"""

from flask import render_template, Blueprint, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func, desc
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import Tabs

from project import db, mail, app
from .forms import RegisterForm, LoginForm, EmailForm, PasswordForm, UsernameForm
from project.models import User, Evaluation, Answer, Evaluation_Likes, Answer_Vote

######
# Helper functions
######
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()

def send_confirmation_email(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
        _external=True)
    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url)
    send_email('Confirm Your Email Address', [user_email], html)

def send_password_reset_email(user_email):
    password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    password_reset_url = url_for(
        'users.reset_with_token',
        token = password_reset_serializer.dumps(user_email, salt='password-reset-salt'),
        _external=True)
    html = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)
    send_email('Password Reset Requested', [user_email], html)

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated = True
                user.last_logged_in = user.current_logged_in
                user.current_logged_in = datetime.now()
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('users.user_profile'))
            else:
                flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('users.login'))

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.email.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                send_confirmation_email(new_user.email)
                return redirect(url_for('evaluations.index'))
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('register.html', form=form)

@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)#one hour time limit
    except:
        flash('Link time out, please register again.','error')
        return redirect(url_for('users.register'))

    user = User.query.filter_by(email=email).first()

    if user.email_confirmed:
        pass
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('evaluations.index'))

@users_blueprint.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return render_template('password_reset_email.html', form=form)

        if user.email_confirmed:
            send_password_reset_email(user.email)
            flash('Please check your email for a password reset link.', 'success')
        else:
            flash('Your email address must be confirmed before attempting a password reset. Email resent', 'error')
            send_confirmation_email(new_user.email) #Resend confirmation email
        return redirect(url_for('users.login'))

    return render_template('password_reset_email.html', form=form)

@users_blueprint.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(token, salt='password-reset-salt', max_age=600)#10 minutes
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('users.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
        except:
            flash('Invalid email address!', 'error')
            return redirect(url_for('users.login'))

        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password_with_token.html', form=form, token=token)

@users_blueprint.route('/user_profile')
@login_required
def user_profile():
    total_questions = Evaluation.query.filter(Evaluation.user_id == current_user.id).count()
    #Right now just by id and not implementing likes
    try:
        top_question = db.session.query(Evaluation.id,Evaluation.evaluation_category,\
                            Evaluation.evaluation_question,func.count(Evaluation_Likes.like).\
                            label('Likes')).outerjoin(Evaluation_Likes).group_by(Evaluation.id).\
                            filter(Evaluation.user_id == current_user.id).order_by(desc('Likes')).first()[2]
    except:
        top_question = "None"
    total_answers = Answer.query.filter(Answer.user_id == current_user.id).count()
    try:
        top_answer = db.session.query(Answer.id,Answer.answer_content,\
                            func.count(Answer_Vote.vote).label('Upvotes')).\
                            outerjoin(Answer_Vote).filter(Answer.user_id == current_user.id).\
                            group_by(Answer.id).order_by(desc('Upvotes')).first()[1]
    except:
        top_answer = "None"
    return render_template('user_profile.html',total_questions=total_questions,top_question=top_question,\
            total_answers=total_answers,top_answer=top_answer)

@users_blueprint.route('/email_change', methods=["GET", "POST"])
@login_required
def user_email_change():
    form = EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user_check = User.query.filter_by(email=form.email.data).first()
                if user_check is None:
                    user = current_user
                    user.email = form.email.data
                    user.email_confirmed = False
                    user.email_confirmed_on = None
                    user.email_confirmation_sent_on = datetime.now()
                    db.session.add(user)
                    db.session.commit()
                    send_confirmation_email(user.email)
                    flash('Email changed!  Please confirm your new email address (link sent to new email).', 'success')
                    return redirect(url_for('users.user_profile'))
                else:
                    flash('Sorry, that email already exists!', 'error')
            except IntegrityError:
                flash('Error! That email already exists!', 'error')
    return render_template('email_change.html', form=form)

@users_blueprint.route('/password_change', methods=["GET", "POST"])
@login_required
def user_password_change():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for('users.user_profile'))

    return render_template('password_change.html', form=form)

@users_blueprint.route('/username_change', methods=["GET", "POST"])
@login_required
def user_username_change():
    form = UsernameForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.username = form.username.data
            db.session.add(user)
            db.session.commit()
            flash('Username has been updated!', 'success')
            return redirect(url_for('users.user_profile'))

    return render_template('username_change.html', form=form)

@users_blueprint.route('/resend_confirmation')
@login_required
def resend_email_confirmation():
    try:
        send_confirmation_email(current_user.email)
        flash('Email sent to confirm your email address.  Please check your email!', 'success')
    except IntegrityError:
        flash('Error!  Unable to send email to confirm your email address.', 'error')

    return redirect(url_for('users.user_profile'))

@users_blueprint.route('/admin_view_users')
@login_required
def admin_view_users():
    if current_user.role != 'admin':
        abort(403)
    else:
        users = User.query.order_by(User.id).all()
        return render_template('admin_view_users.html', users=users)
    return redirect(url_for('users.user_profile'))

'''
Developing a dashboard for admin views

Current status
For a dataframe, create a histogram of each column except the last

Have a dropdown menu to change between columns in the DataFrame

Dynamic plotting

Hover tools but they are broken right now

'''
# Load the Iris Data Set
iris = load_iris()
iris_df = pd.DataFrame(data= np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])
feature_names = iris_df.columns[0:-1].values.tolist()

# Create the main plot
def create_figure(current_feature_name, bins):
    hist, edges = np.histogram(iris_df[current_feature_name], bins = bins)

    hist_df = pd.DataFrame({current_feature_name: hist, "left": edges[:-1], "right": edges[1:]})
    hist_df["interval"] = ["%d to %d" % (left, right) for left, right in zip(hist_df["left"], hist_df["right"])]

    src = ColumnDataSource(hist_df)

    p = figure(plot_height = 600, plot_width = 600, title = "Histogram of {}".format(current_feature_name.capitalize()),\
            x_axis_label = current_feature_name.capitalize(), y_axis_label = "Count")

    p.quad(bottom = 0, top = current_feature_name,left = "left", right = "right", source = src, fill_color = "SteelBlue",\
            line_color = "black", fill_alpha = 0.7, hover_fill_alpha = 1.0, hover_fill_color = "Tan")

    hover = HoverTool(tooltips = [('Interval', '@interval'), ('Count', str("@" + current_feature_name))])
    p.add_tools(hover)
    return p

@users_blueprint.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    else:
        current_feature_name = request.args.get("feature_name")
        if current_feature_name == None:
            current_feature_name = "sepal length (cm)"

        plot = create_figure(current_feature_name, 10)
        script, div = components(plot)

        return render_template('admin_dashboard.html', script=script, div=div,\
                feature_names=feature_names,  current_feature_name=current_feature_name)

    return redirect(url_for('users.user_profile'))

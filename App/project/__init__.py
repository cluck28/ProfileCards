#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 12:56:08 2018

@author: christopherluciuk
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from elasticsearch import Elasticsearch

app = Flask(__name__, instance_relative_config = True)
app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from project.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

from project.users.views import users_blueprint
from project.evaluations.views import evaluations_blueprint
from project.answers.views import answers_blueprint

#register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(evaluations_blueprint)
app.register_blueprint(answers_blueprint)

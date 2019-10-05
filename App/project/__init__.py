#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 12:56:08 2018

@author: christopherluciuk
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config = True)
app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.evaluations.views import evaluations_blueprint

#register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(evaluations_blueprint)

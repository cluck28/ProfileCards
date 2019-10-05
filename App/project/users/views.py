#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 5, 2019

@author: christopherluciuk
"""

from flask import render_template, Blueprint

users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    '''
    Render the login page
    '''
    return render_template('login.html')

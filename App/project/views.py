#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 5, 2019

@author: christopherluciuk
"""

from flask import render_template, request, url_for, redirect
from project import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

# Python code to connect to Postgres
'''user = 'christopherluciuk'
host = 'localhost'
dbname = 'ONET_db_v2'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)'''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    '''
    Render the landing page
    '''
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    '''
    Render the login page
    Simple admin credentials implemented
    '''
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

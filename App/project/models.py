# project/models.py

from project import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime

class Answer(db.Model):

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer_content = db.Column(db.String, nullable=False)
    answer_upvotes = db.Column(db.Integer, nullable=False)
    answer_created_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, content):
        self.answer_content = content
        self.answer_created_on = datetime.now()
        self.answer_upvotes = 0

    def __repr__(self):
        return '<title {}'.format(self.name)

class Evaluation(db.Model):

    __tablename__ = "evaluations"

    id = db.Column(db.Integer, primary_key=True)
    evaluation_category = db.Column(db.String, nullable=False)
    evaluation_question = db.Column(db.String, nullable=False)
    evaluation_difficulty = db.Column(db.Integer, nullable=False)
    evaluation_likes = db.Column(db.Integer, nullable=False)
    evaluation_created_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, category, question):
        self.evaluation_category = category
        self.evaluation_question = question
        self.evaluation_created_on = datetime.now()
        self.evaluation_difficulty = 0
        self.evaluation_likes = 0

    def __repr__(self):
        return '<title {}'.format(self.name)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    username = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, default='user')

    def __init__(self, email, plaintext_password, email_confirmation_sent_on=None, role='user'):
        self.email = email
        self.password = plaintext_password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.username = email
        self.role = role

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

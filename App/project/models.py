# project/models.py

from project import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

class Evaluation(db.Model):

    __tablename__ = "evaluations"

    id = db.Column(db.Integer, primary_key=True)
    evaluation_title = db.Column(db.String, nullable=False)
    evaluation_category = db.Column(db.String, nullable=False)
    evaluation_question = db.Column(db.String, nullable=False)

    def __init__(self, title, category, question):
        self.evaluation_title = title
        self.evaluation_category = category
        self.evaluation_question = question

    def __repr__(self):
        return '<title {}'.format(self.name)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, plaintext_password):
        self.email = email
        self.password = plaintext_password
        self.authenticated = False

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

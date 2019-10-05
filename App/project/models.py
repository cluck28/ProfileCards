# project/models.py

from project import db

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

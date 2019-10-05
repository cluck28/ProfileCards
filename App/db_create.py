from project import db
from project.models import Evaluation

# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

# insert recipe data
evaluation = Evaluation('Linear Regression', 'Machine Learning','Derive linear regression.')

db.session.add(evaluation)

# commit the changes
db.session.commit()

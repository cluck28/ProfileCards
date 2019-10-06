from project import db
from project.models import Evaluation, User

# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

# insert user data
#user1 = User('csluciuk@gmail.com', 'password1234')
#user2 = User('insightuser@gmail.com', 'PaSsWoRd')
#user3 = User('blaa@blaa.com', 'MyFavPassword')
#db.session.add(user1)
#db.session.add(user2)
#db.session.add(user3)

# insert evaluation data
evaluation = Evaluation('Linear Regression', 'Machine Learning','Derive linear regression.')

db.session.add(evaluation)

# commit the changes
db.session.commit()

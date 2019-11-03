from project import db
from project.models import Evaluation, User, Answer, Evaluation_Likes, Answer_Vote, Evaluation_Difficulty
import pandas as pd

#Load emails and password from csv
#filename = ""
df = pd.read_csv(filename)

for index, row in df.iterrows():
    user = User(email=row['email'], plaintext_password=row['password'],role=row['role'])
    db.session.add(user)

db.session.commit()

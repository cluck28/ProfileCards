from project import db
from project.models import Evaluation, User, Answer, Evaluation_Likes, Answer_Vote, Evaluation_Difficulty
import pandas as pd

#Load emails and password from csv
#filename = ""
df = pd.read_csv(filename)

ADMIN_ID = 1

for index, row in df.iterrows():
    question = Evaluation(row['category'], row['question'], ADMIN_ID)
    db.session.add(question)
    db.session.flush()
    rating = Evaluation_Difficulty(ADMIN_ID,question.id,row['difficulty'])
    db.session.add(new_rating)

db.session.commit()

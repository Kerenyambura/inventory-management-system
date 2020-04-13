from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:Goodmand254@localhost:5432/alchemist' 
db=SQLAlchemy(app) 


class User(db.Model):

    id=db.Column(db.Integer,primary_key=True)     
    username=db.Column(db.String,unique=True,nullable=False)     
    email=db.Column(db.String,unique=True,nullable=False)

    def __repr__(self): 
        return "Username: {} and Email: {}".format(self.username,self.email)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return 'Hello World!'



if __name__== "__main__":
    app.run()
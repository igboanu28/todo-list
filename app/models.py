from app import  db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
import jwt
from app import app




"""
    My Task model should have the follwing
    - id
    - name : str
    - complete : bool
"""

class Task(db.Model):
    task_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    complete=db.Column(db.Boolean)
    #Foreign Key to link users (refer to primary key of the user)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Task {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # User can have many task
    
    about_me = db.Column(db.String(140))
    
    tasks = db.relationship('Task', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)
 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
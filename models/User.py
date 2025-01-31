from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    name = db.Column(db.String(150), nullable=False)
  
    

    incomes = db.relationship('Income', backref='user_incomes')  
    expenses = db.relationship('Expense', backref='user_expenses') 

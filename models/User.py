from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default= False)
  
    

    incomes = db.relationship('Income', back_populates='user')
    
    expenses = db.relationship('Expense', back_populates='user')

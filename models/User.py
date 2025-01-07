from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Nome explícito para a tabela
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Relacionamento com as receitas (incomes)
    incomes = db.relationship('Income', backref='user_incomes')  # Nome do backref alterado
    expenses = db.relationship('Expense', backref='user_expenses')  # Nome do backref alterado

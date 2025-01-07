from db import db

class Expense(db.Model):
    __tablename__ = 'expenses'  
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

    user = db.relationship('User', backref='user_expenses')  
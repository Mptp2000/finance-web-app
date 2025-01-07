from db import db

class Income(db.Model):
    __tablename__ = 'incomes'  # Nome explícito para a tabela
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Chave estrangeira para 'users'

    user = db.relationship('User', backref='user_incomes')  # Modificado o backref para 'user_incomes'

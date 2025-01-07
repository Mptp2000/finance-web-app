
from models import Income, Expense
from db import db

def calculate_net_worth(user_id):
    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0
    total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0
    return total_income - total_expenses

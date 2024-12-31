from db import db
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class Transaction(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    type  = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
  

    def __repr__(self):
        return f'<Transaction {self.category} - {self.type} - {self.amount}>'

    # Método para validar o valor
    def validate(self):
        if self.amount <= 0:
            return False, "O valor da transação deve ser maior que zero."
        return True, None

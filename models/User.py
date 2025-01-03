from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


    # Método para definir a senha
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Método para verificar a senha
    def check_password(self, password):
        return check_password_hash(self.password, password)

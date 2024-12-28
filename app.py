from flask import Flask, render_template, request, redirect, url_for, flash
from db import db
from models.transaction import Transaction
from datetime import datetime
from config import Config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.User import User

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'seu_segredo_seguro'

# Configuração do login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Define a página de login como padrão para usuários não autenticados

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Corrigido para buscar por `user_id`

# Banco de dados
db.init_app(app)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Você deve usar um hash seguro para armazenar senhas
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))  # Redireciona para a página principal
        else:
            flash('Credenciais inválidas!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Página inicial
@app.route('/')
@login_required  # Protege a rota para que somente usuários autenticados possam acessá-la
def index():
    transactions = Transaction.query.all()
    return render_template('index.html', transactions=transactions)

# Lista de transações
@app.route('/transactions')
@login_required  # Protege a rota
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

# Adicionar transação
@app.route('/add_transaction', methods=['POST'])
@login_required  # Protege a rota
def add_transaction():
    transaction_type = request.form['type']
    category = request.form['category']
    amount = request.form['amount']
    date_str = request.form['date']

    if not transaction_type or not category or not amount or not date_str:
        flash("Todos os campos são obrigatórios!", "danger")
        return redirect(url_for('index'))

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
        return redirect(url_for('index'))

    new_transaction = Transaction(
        type=transaction_type,
        category=category,
        amount=amount,
        date=date
    )
    db.session.add(new_transaction)
    db.session.commit()

    flash("Transação adicionada com sucesso!", "success")
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

# Criar tabelas antes da primeira solicitação
@app.before_request
def create_tables():
    db.create_all()



@app.before_request
def create_test_user():
    db.create_all()  # Cria as tabelas se ainda não existirem
    if not User.query.filter_by(username='admin').first():
        test_user = User(
            username='admin',
            password='123456'  # IMPORTANTE: Em um ambiente real, use hashing para senhas
        )
        db.session.add(test_user)
        db.session.commit()
        print("Usuário de teste criado: admin / 123456")


if __name__ == "__main__":
    app.run(debug=True)

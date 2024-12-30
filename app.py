from flask import Flask, render_template, request, redirect, url_for, flash
from db import db  # A instância db deve ser importada do arquivo db.py
from models.transaction import Transaction
from datetime import datetime
from config import Config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import locale
# Configura o local para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')







# Criação da aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)




# Inicializando a instância do SQLAlchemy (somente uma vez)
db.init_app(app)  # Esta linha garante que o Flask app use o db corretamente

# Configuração do login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Define a página de login como padrão para usuários não autenticados

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Banco de dados
# db.init_app(app)  # Remover esta linha porque já está sendo inicializado anteriormente.

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Tenta encontrar o usuário no banco de dados
        user = User.query.filter_by(username=username).first()

        if user:
            # Verifica se a senha fornecida corresponde à senha armazenada (criptografada)
            if check_password_hash(user.password, password):
                login_user(user)  # Faz o login do usuário
                flash('Login bem-sucedido!', 'success')
                return redirect(url_for('index'))  # Redireciona para a página de transações
            else:
                flash('Senha incorreta.', 'error')  # Exibe mensagem de erro se a senha estiver incorreta
        else:
            flash('Usuário não encontrado.', 'error')  # Exibe mensagem de erro se o usuário não for encontrado
            
    return render_template('login.html')
    
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
    valor = sum(transaction.amount for transaction in transactions )
    valor_formatado = locale.currency(valor, grouping=True)


    
    return render_template('transactions.html', transactions=transactions, valor_formatado=valor_formatado)

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
        date=date,
       
    )
    db.session.add(new_transaction)
    db.session.commit()

    flash("Transação adicionada com sucesso!", "success")
    return redirect(url_for('index'))

# Editar transação
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if request.method == 'POST':
        transaction.type = request.form['type']
        transaction.category = request.form['category']
        transaction.amount = request.form['amount']
        date_str = request.form['date']

        try:
            transaction.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
            return redirect(url_for('edit_transaction', id=id))

        db.session.commit()

        flash("Transação atualizada com sucesso!", "success")
        return redirect(url_for('index'))

    return render_template('edit_transaction.html', transaction=transaction)

# Excluir transação
@app.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()

    flash("Transação excluída com sucesso!", "success")
    return redirect(url_for('transactions'))

# Rota para logout
@app.route('/logout')
@login_required  # Garante que apenas usuários autenticados possam fazer logout
def logout():
    logout_user()  # Faz o logout do usuário
    return redirect(url_for('login'))  # Redireciona para a página de login


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Verificar se as senhas coincidem
        if password != password_confirm:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        # Verificar se o nome de usuário já existe
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Nome de usuário já existe', 'danger')
            return redirect(url_for('register'))

        # Criptografar a senha antes de salvar no banco
        hashed_password = generate_password_hash(password)

        # Criar o novo usuário com a senha criptografada
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Criar tabelas antes da primeira solicitação
@app.before_request
def create_tables():
    db.create_all()


# Crie um filtro customizado para formatar a moeda
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return locale.currency(value, grouping=True)
    except:
        return value  # Caso falhe, retorna o valor sem formatação    




app.run(debug=True)        

from flask import Flask, render_template, request, redirect, url_for, flash
from db import db  # A instância db deve ser importada do arquivo db.py
from models.transaction import Transaction
from datetime import datetime
from config import Config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


# Criação da aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializando a instância do SQLAlchemy (somente uma vez)
db.init_app(app)  # Esta linha garante que o Flask app use o db corretamente

# Função para excluir todos os usuários, exceto o admin
def delete_all_users_except_admin():
    with app.app_context():  # Garante que o código rode dentro do contexto da aplicação
        users = User.query.all()
        for user in users:
            if user.username != 'admin':
                db.session.delete(user)
        db.session.commit()
        print("Usuários excluídos com sucesso, exceto o admin.")

# Função para criar um novo usuário admin
def create_admin_user():
    with app.app_context():  # Garante que o código rode dentro do contexto da aplicação
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password=generate_password_hash('123456'))
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso.")
        else:
            print("Usuário admin já existe.")

# Código principal para executar as funções
if __name__ == "__main__":
    # Garante que a aplicação esteja rodando antes de executar as funções
    with app.app_context():  # Garantindo que o contexto da aplicação esteja disponível
        delete_all_users_except_admin()
        create_admin_user()

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
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()

    flash("Transação excluída com sucesso!", "success")
    return redirect(url_for('index'))

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

@app.before_request
def create_test_user():
    db.create_all()  # Cria as tabelas se ainda não existirem
    if not User.query.filter_by(username='admin').first():
        test_user = User(
            username='admin',
            password=generate_password_hash('123456')  # Criptografa a senha do usuário de teste
        )
        db.session.add(test_user)
        db.session.commit()
        print("Usuário de teste criado: admin / 123456")



# Função para criar o usuário administrador
def create_admin_user():
    with app.app_context():  # Garante que o código rode dentro do contexto da aplicação
        # Verifica se o usuário admin já existe
        admin = User.query.filter_by(username='MTP').first()
        if not admin:
            # Criptografa a senha e cria o usuário admin
            admin = User(username='MTP', password=generate_password_hash('123456'))
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso.")
        else:
            print("Usuário admin já existe.")

# Chama a função para criar o administrador
create_admin_user()


if __name__ == "__main__":
    app.run(debug=True)

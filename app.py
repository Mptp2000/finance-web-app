from flask import Flask, render_template, request, redirect, url_for, flash
from db import db

from models.User import User
from models.income import Income  
from models.expense import Expense  
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from config import Config
import locale


# Configura o local para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Criação da aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializando a instância do SQLAlchemy
db.init_app(app)

# Configuração do login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas.', 'error')

    return render_template('login.html')

# Página inicial
@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))


# Adicionar transação
@app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    transaction_type = request.form['type']
    category = request.form['category']
    amount = request.form['amount']
    date_str = request.form['date']

    if not transaction_type or not category or not amount or not date_str:
        flash("Todos os campos são obrigatórios!", "danger")
        return redirect(url_for('transactions'))

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
        return redirect(url_for('transactions'))

    new_transaction = Transaction(type=transaction_type, category=category, amount=float(amount), date=date)
    db.session.add(new_transaction)
    db.session.commit()

    flash("Transação adicionada com sucesso!", "success")
    return redirect(url_for('transactions'))

# Editar transação
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if request.method == 'POST':
        # Captura os dados do formulário
        transaction_type = request.form['type']
        category = request.form['category']
        amount = request.form['amount']
        date_str = request.form['date']

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
            return redirect(url_for('edit_transaction', id=id))

        
        # Atualiza os dados da transação
        transaction.type = transaction_type
        transaction.category = category
        transaction.amount = float(amount)  
        transaction.date = date    

        db.session.commit()
        flash("Transação atualizada com sucesso!", "success")
        return redirect(url_for('transactions'))

    return render_template('edit_transaction.html', transaction=transaction)

# Excluir transação
@app.route('/delete/<int:id>')
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()

    flash("Transação excluída com sucesso!", "success")
    return redirect(url_for('transactions'))

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Nome de usuário já existe', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id

    # Calcula o total de receitas
    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=user_id).scalar() or 0
    # Calcula o total de despesas
    total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=user_id).scalar() or 0

    # Calcula o patrimônio líquido
    net_worth = total_income - total_expenses

    # Consulta as receitas e despesas para exibição
    incomes = Income.query.filter_by(user_id=user_id).all()
    expenses = Expense.query.filter_by(user_id=user_id).all()

    # Retorna o render do template dashboard.html
    return render_template('dashboard.html', total_income=total_income, total_expenses=total_expenses, net_worth=net_worth, incomes=incomes, expenses=expenses)


from datetime import datetime

@app.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    if request.method == 'POST':
        amount = float(request.form['amount'])  # Convertendo para float
        description = request.form['description']
        date_str = request.form['date']
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Converte para data
        except ValueError:
            flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
            return redirect(url_for('add_income'))

        new_income = Income(amount=amount, description=description, date=date, user_id=current_user.id)
        db.session.add(new_income)
        db.session.commit()

        flash("Receita adicionada com sucesso!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_income.html')




@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Captura os valores enviados pelo formulário
        amount = request.form['amount']
        description = request.form['description']
        date_str = request.form['date']


        date = datetime.strptime(date_str,  '%Y-%m-%d').date()
 
        new_expense= Expense(amount=amount, description=description,date=date, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()
        

    

     
        return redirect(url_for('dashboard'))  # Redireciona para o dashboard
    return render_template('add_expense.html')






@app.route('/logout')
@login_required
def logout():
    logout_user()  # Desloga o usuário
    return redirect(url_for('login'))  # Redireciona para a página de login


# Criação de tabelas na inicialização
@app.before_request
def create_tables():
    db.create_all()

# Filtro personalizado para formatação de moeda
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return locale.currency(value, grouping=True)
    except Exception:
        return value


@app.route('/edit_income/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_income(id):
    income = Income.query.get_or_404(id)

    if request.method == 'POST':
        income.amount = request.form['amount']
        income.description = request.form['description']
        date_str = request.form['date']

        try:
            income.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
            return redirect(url_for('edit_income', id=id))

        db.session.commit()
        flash("Receita atualizada com sucesso!", "success")
        return redirect(url_for('dashboard'))

    return render_template('edit_income.html', income=income)

@app.route('/delete_income/<int:id>', methods=['GET'])
@login_required
def delete_income(id):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()

    flash("Receita excluída com sucesso!", "success")
    return redirect(url_for('dashboard'))



@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if request.method == 'POST':
        expense.amount = request.form['amount']
        expense.description = request.form['description']
        date_str = request.form['date']
        
        try:
            expense.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
            return redirect(url_for('edit_expense', id=id))
        
        db.session.commit()
        flash("Despesa atualizada com sucesso!", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('edit_expense.html', expense=expense)

@app.route('/delete_expense/<int:id>', methods=['GET'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()

    flash("Despesa excluída com sucesso!", "success")
    return redirect(url_for('dashboard'))




# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)

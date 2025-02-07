from flask import Flask, render_template, request, redirect, url_for, flash
from models.User import User
from models.income import Income  
from models.expense import Expense  
from models.forms import EditProfileForm, RegisterForm


from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
from config import Config
import locale
from flask_migrate import Migrate

from werkzeug.security import check_password_hash, generate_password_hash
from db import db  
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
    
# Configura o local para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Criação da aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializando a instância do SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)



# Configuração do login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))



@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Tentando fazer login com: {username} / {password}")  # Verifique no console
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas.', 'error')
            print("Credenciais inválidas")  # Verifique se o login está falhando

    return render_template('login.html')
    
# Página inicial
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password_confirm = form.password_confirm.data
        name = form.name.data
        email = form.email.data

        # Verifica se as senhas coincidem
        if password != password_confirm:
            flash('As senhas não coincidem. Tente novamente.', 'danger')
            return redirect(url_for('register'))

        # Verifica se o nome de usuário já existe
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Nome de usuário já existe. Escolha outro.', 'danger')
            return redirect(url_for('register'))

        try:
            # Criptografa a senha
            hashed_password = generate_password_hash(password)

            # Cria o novo usuário
            new_user = User(username=username, password=hashed_password, name=name, email=email)
            db.session.add(new_user)
            db.session.commit()

            flash('Usuário registrado com sucesso! Agora faça login.', 'success')
            return redirect(url_for('user_login'))

        except Exception as e:
            # Caso haja algum erro no processo de registro, exibe uma mensagem
            flash(f'Ocorreu um erro ao registrar o usuário: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)
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

    return render_template('dashboard.html', total_income=total_income, total_expenses=total_expenses, net_worth=net_worth, incomes=incomes, expenses=expenses)

# Rota para adicionar uma receita
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

# Rota para adicionar uma despesa
@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])  # Convertendo para float
        description = request.form['description']
        date_str = request.form['date']
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Data inválida. Use o formato YYYY-MM-DD.", "danger")
            return redirect(url_for('add_expense'))

        new_expense = Expense(amount=amount, description=description, date=date, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()

        flash("Despesa adicionada com sucesso!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_expense.html')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Desloga o usuário
    flash('Deslogado com sucesso', 'success')
    return redirect(url_for('user_login'))  # Redireciona para a página de login

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

# Editar receita
@app.route('/edit_income/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_income(id):
    income = Income.query.get_or_404(id)

    if request.method == 'POST':
        income.amount = float(request.form['amount'])  # Convertendo para float
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

# Excluir receita
@app.route('/delete_income/<int:id>', methods=['GET'])
@login_required
def delete_income(id):
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()

    flash("Receita excluída com sucesso!", "success")
    return redirect(url_for('dashboard'))

# Editar despesa
@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if request.method == 'POST':
        expense.amount = float(request.form['amount'])  # Convertendo para float
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

# Excluir despesa
@app.route('/delete_expense/<int:id>', methods=['GET'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()

    flash("Despesa excluída com sucesso!", "success")
    return redirect(url_for('dashboard'))

# Perfil do usuário
@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    return render_template('perfil.html', user=current_user)

# Editar perfil
@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = EditProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil'))  

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name

    return render_template('editar_perfil.html', form=form)

# Trocar senha
@app.route('/trocar_senha', methods=['GET', 'POST'])
@login_required
def trocar_senha():
    return render_template('trocar_senha.html')


@app.route('/relatorios')
@login_required
def relatorios():
    user_id = current_user.id

    # Filtrar transações do usuário logado
    expenses = Expense.query.filter_by(user_id=user_id).all()
    incomes = Income.query.filter_by(user_id=user_id).all()

    # Calcular totais
    total_income = sum(income.amount for income in incomes)  # Soma todas as receitas
    total_expense = sum(expense.amount for expense in expenses)  # Soma todas as despesas

    balance = total_income - total_expense

    return render_template('relatorios.html', 
                           expenses = expenses,
                           incomes = incomes,
                           total_income=total_income, 
                           total_expense=total_expense, 
                           balance=balance)





# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)

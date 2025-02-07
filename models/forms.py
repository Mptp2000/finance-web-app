from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo,Regexp

class EditProfileForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    name = StringField('Nome', validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField('Salvar Alterações')


     
#Edição de Perfil#


class RegisterForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    name = StringField('Nome Completo', validators=[DataRequired(), Length(min=3, max=50)])
    
    # Campo de senha
    password = PasswordField('Senha', validators=[
        DataRequired(), 
        Length(min=8, message="A senha deve ter no mínimo 8 caracteres"),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', message="A senha deve conter pelo menos uma letra, um número e um caractere especial")
    ])
    
    # Confirmação de senha
    password_confirm = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('password', message="As senhas devem coincidir")
    ])
    
    submit = SubmitField('Registrar')

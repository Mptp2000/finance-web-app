from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class EditProfileForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    name = StringField('Nome', validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField('Salvar Alterações')


     
#Edição de Perfil#
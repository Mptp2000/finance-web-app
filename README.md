
# Finance Web App

Aplicação web simples para controle de finanças pessoais usando Flask.

## Descrição

O **Finance Web App** é uma aplicação de controle de finanças pessoais desenvolvida com o framework **Flask**. Ele permite aos usuários registrar, editar, excluir e visualizar transações financeiras. A aplicação oferece autenticação de usuários, além de funcionalidades como o cálculo de um total de despesas e receitas.

## Funcionalidades

- **Cadastro de Usuários:** Possibilidade de registro e login de usuários.
- **Controle de Transações:** Adicionar, editar e excluir transações financeiras (Receitas/Despesas).
- **Visualização das Transações:** Exibição das transações registradas em uma tabela com valores formatados.
- **Autenticação:** Apenas usuários autenticados podem acessar o sistema e suas transações.
- **Cálculo de Total:** Exibe o total das transações registradas (receitas e despesas).
- **Segurança:** Senhas dos usuários são armazenadas de forma segura usando hashing.

## Tecnologias Utilizadas

- **Flask:** Framework para desenvolvimento da aplicação web.
- **SQLAlchemy:** ORM (Object Relational Mapper) para interagir com o banco de dados.
- **SQLite:** Banco de dados utilizado para armazenar as transações e usuários.
- **Flask-Login:** Para gerenciamento de sessões de usuários.

## Requisitos

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug
- Locale (para formatação de moeda)

## Como Executar o Projeto

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/Mptp2000/finance-web-app.git
   cd finance-web-app
Instalar as dependências:

Se você ainda não tem o pip instalado, você pode instalar as dependências com o seguinte comando:

bash

pip install -r requirements.txt
Se o arquivo requirements.txt não estiver presente, você pode instalar as dependências manualmente com:

bash

pip install flask flask_sqlalchemy flask_login werkzeug
Criar o banco de dados:

A primeira vez que você rodar a aplicação, o banco de dados será criado automaticamente:

bash

flask shell
>>> from db import db, init_app
>>> init_app(app)
Executar a aplicação:

Para iniciar o servidor de desenvolvimento:

bash

flask run
A aplicação estará disponível em http://127.0.0.1:5000.

Como Usar
Cadastro e Login:

Acesse a página de login em /login.
Se você ainda não tem uma conta, crie uma em /register.
Adicionar Transações:

Após o login, você será redirecionado para a página inicial onde pode adicionar novas transações financeiras.
Visualizar e Gerenciar Transações:

Na página de transações (/transactions), você pode ver a lista de transações, editar ou excluir.
Logout:

Para sair da sua conta, basta clicar no botão "Logout".
Contribuição
Se você gostaria de contribuir para este projeto, por favor, faça um fork do repositório e envie um pull request com suas melhorias.

Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

markdown

### Explicação:

1. **Descrição:** Explica o propósito e as funcionalidades principais da aplicação.
2. **Tecnologias Utilizadas:** Lista as tecnologias e bibliotecas usadas.
3. **Requisitos:** Instruções sobre o que é necessário para executar o projeto.
4. **Como Executar o Projeto:** Passos claros para clonar, instalar dependências, e executar o projeto localmente.
5. **Como Usar:** Instruções de uso da aplicação após a instalação.
6. **Contribuição e Licença:** Seções sobre como contribuir para o projeto e a licença associada.







class Config:
    SECRET_KEY = 'sua_chave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///finance_app.db'  # Verifique se o caminho está correto
    SQLALCHEMY_TRACK_MODIFICATIONS = False

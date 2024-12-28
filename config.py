class Config:
    SECRET_KEY = 'CLSKE10943051'  # Deve ser alterada em produção para um valor mais seguro
    SQLALCHEMY_DATABASE_URI = 'sqlite:///finance.db'  # Caminho do banco de dados SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa o rastreamento de modificações do banco
    SESSION_COOKIE_SECURE = True  # Assegura que cookies de sessão sejam transmitidos apenas via HTTPS (em produção)

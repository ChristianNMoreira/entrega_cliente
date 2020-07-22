class Config:
    SECRET_KEY = 'i3zZgZIQe4sECPN485loyTLLPzIKbeTh9wACbstEBHevMKOMslO9DWTEkQjyC3z'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/cmore/OneDrive/Documentos/Entrega_cliente/backend/data.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = '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'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    JWT_SECRET_KEY = SECRET_KEY
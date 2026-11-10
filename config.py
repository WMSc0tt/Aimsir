import os
 
 
class Config:
    # Secret key used by Flask-WTF to protect the forms
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aimsir_secret_key'
 
    # PostgreSQL connection details (same environment variables as initialise_db.py)
    DB_NAME = os.environ.get('AIMSIR_DB_NAME', 'aimsir_db')
    DB_USER = os.environ.get('AIMSIR_DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('AIMSIR_DB_PASSWORD', 'postgres_password') 
    DB_HOST = os.environ.get('AIMSIR_DB_HOST', 'localhost')
    DB_PORT = os.environ.get('AIMSIR_DB_PORT', '5432')
 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
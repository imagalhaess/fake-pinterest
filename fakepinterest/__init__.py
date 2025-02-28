# criar aplicativo, banco de dados, estrutura geral
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
print(os)  # Adiciona esta linha para verificar se "os" está importado corretamente

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "e4a8bb04-0083-4472-bf7a-405a0b361b38c9a695dcb69344bc678144d458a3789a"

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/fotos_posts")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER) # cria a pasta se não existir
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage' # define a página inicial como a de controle de login
login_manager.login_message = 'Faça login para acessar esta página'

from fakepinterest import routes
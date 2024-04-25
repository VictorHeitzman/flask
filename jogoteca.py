from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from config import os

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
app.app_context().push()

csrf = CSRFProtect(app)
bcript = Bcrypt(app)
from views_games import *
from views_user import *


if __name__ == '__main__':
    port =  int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
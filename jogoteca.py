from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
app.app_context().push()

csrf = CSRFProtect(app)
bcript = Bcrypt(app)
from views_games import *
from views_user import *


if __name__ == '__main__':
    app.run(debug=True)
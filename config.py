import os

SECRET_KEY = 'VictorHeitzman'
 
URI = 'sqlite:///dbCrudFlask.db'

SQLALCHEMY_DATABASE_URI = URI

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

METHODS = ['POST','GET']
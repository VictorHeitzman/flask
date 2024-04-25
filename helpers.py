import os
from jogoteca import app, session
from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField

class FormularioJogo(FlaskForm):
    nome        = StringField('Nome do Jogo',   [validators.DataRequired(), validators.length(min=1, max=50)])
    categoria   = StringField('Categoria',      [validators.DataRequired(), validators.length(min=1, max=40)])
    console     = StringField('Console',        [validators.DataRequired(), validators.length(min=1, max=20)])
    salvar      = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nome        = StringField('Nome',           [validators.DataRequired(), validators.length(min=1, max=50)])
    senha       = PasswordField('Senha',        [validators.DataRequired(), validators.length(min=1, max=50)])
    login       = SubmitField('Login')

def validaSessao():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return False
    else:
        return True
    
def recuperaImagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'

def deletaArquivo(id):
    arquivo = recuperaImagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo)) 
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import FormularioJogo, validaSessao, recuperaImagem, deletaArquivo
import time

@app.route('/')
def index():
    listaDeJogos = Jogos.query.order_by(Jogos.id)
    return render_template('index.html', titulo = 'Menos Cores', listaDeJogos = listaDeJogos)

@app.route('/novo')
def novo():
    if validaSessao():
        form = FormularioJogo()
        return render_template('novo.html', titulo = 'Novo Jogo', form = form)
    else:
        return redirect(url_for('login', proxima_pagina=url_for('novo') ))

@app.route('/editar/<int:id>')
def editar(id):
    if validaSessao():
        jogo = Jogos.query.filter_by(id=id).first()
        
        form = FormularioJogo()
        form.nome.data      = jogo.nome
        form.categoria.data = jogo.categoria
        form.console.data   = jogo.console

        capa_jogo = recuperaImagem(id)
        return render_template('editar.html', titulo=f"Editar {jogo.nome}", id=id, capa_jogo=capa_jogo, form=form) 
    else:
        return redirect(url_for('login', proxima_pagina=url_for('editar')))

@app.route('/uploads/<nome_arquivo>')
def uploads(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


##################################################
# FUNCTIONS INTERMEDIARIAS
##################################################

@app.route('/intermed_recuperaJogo/<int:id>')
def intermed_recuperaJogo(id):
    return recuperaImagem(id)


@app.route('/intermed_criar', methods=app.config['METHODS'])
def intermed_criar():
    form = FormularioJogo(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))
    
    nome        = form.nome.data
    categoria   = form.categoria.data
    console     = form.console.data
    arquivo     = request.files['arquivo']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome = nome, categoria = categoria, console = console)
    db.session.add(novo_jogo)
    db.session.commit()

    
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{novo_jogo.nome}.jpg')

    return redirect(url_for('index'))

@app.route('/intermed_logout')
def intermed_logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))

@app.route('/intermed_deletar/<int:id>')
def intermed_deletar(id):
    jogo        = Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo Deletado!')
    return redirect(url_for('index'))

@app.route('/intermed_editar', methods=app.config['METHODS'])
def intermed_editar():
    form = FormularioJogo(request.form)
    if form.validate_on_submit():

        jogo            = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome       = form.nome.data
        jogo.categoria  = form.categoria.data
        jogo.console    = form.console.data
        db.session.add(jogo)
        db.session.commit()

        arquivo     = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestemp = time.time()
        deletaArquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestemp}.jpg')
    
    return redirect(url_for('index'))




from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Jogos, Usuarios
from helpers import FormularioUsuario
from jogoteca import app, db
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    form = FormularioUsuario()

    proxima = request.args.get('proxima_pagina')
    return render_template('login.html', proxima_pagina=proxima, form=form)


@app.route('/adicionar')
def adicionar():
    form    = FormularioUsuario()
    return render_template('adicionar.html', titulo  = 'Adicionar Usuario', form=form)

@app.route('/intermed_novoUser', methods=app.config['METHODS'])
def intermed_novoUser():
    form    = FormularioUsuario(request.form)

    nome    = form.nome.data
    senha   = form.senha.data
    novo_usuario = Usuarios.query.filter_by(nome = nome).first()
    
    if  not novo_usuario:
        db.session.add(Usuarios(nome=nome, senha=senha))
        db.session.commit()
        flash('Usuario Adicionado com sucesso!')
        return redirect('login')
    flash('Usuario já adicionado, tente outro!')
    return redirect('adicionar')

@app.route('/intermed_autenticar', methods=app.config['METHODS'])
def intermed_autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nome = form.nome.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
            session['usuario_logado'] = usuario.nome
            flash(usuario.nome +' logado com sucesso!')
            proxima_pagina = request.form['proxima_pagina'].replace("/","")
        if proxima_pagina != 'None':
            return redirect(url_for(proxima_pagina))
        else: 
            return redirect(url_for('index'))
    else:
        flash('Usuario não logado!')
        return redirect(url_for('login'))
    

#   VALIDAÇÃO DE SENHA HASH
# @app.route('/intermed_autenticar', methods=app.config['METHODS'])
# def intermed_autenticar():
#     form = FormularioUsuario(request.form)
#     usuario = Usuarios.query.filter_by(nome = form.nome.data).first()
#     senha = check_password_hash(usuario.senha, form.senha.data)
#     if usuario and senha:
#         session['usuario_logado'] = usuario.nome
#         flash(usuario.nome +' logado com sucesso!')
#         proxima_pagina = request.form['proxima_pagina'].replace("/","")
#         if proxima_pagina != 'None':
#             return redirect(url_for(proxima_pagina))
#         else: 
#             return redirect(url_for('index'))
#     else:
#         flash('Usuario não logado!')
#         return redirect(url_for('login'))

#pip install Werkzeug
# criar as rotas do site (links)
from flask import render_template, url_for, redirect, request
from fakepinterest import app
from fakepinterest import bcrypt, database
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename


@app.route('/', methods=["POST", "GET"])
def homepage():
   form_login = FormLogin()
   if form_login.validate_on_submit():
      usuario = Usuario.query.filter_by(email=form_login.email.data).first()
      if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
         login_user(usuario)
         return redirect(url_for('perfil', id_usuario=usuario.id))
   return render_template('homepage.html', form=form_login)


@app.route('/criar_conta', methods=["POST", "GET"])
def criar_conta():
   form_criarconta = FormCriarConta()
   if form_criarconta.validate_on_submit(): 
      senha = bcrypt.generate_password_hash(form_criarconta.senha.data)
      usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha)

      database.session.add(usuario)
      database.session.commit()
      login_user(usuario, remember=True)
      return redirect(url_for('perfil', id_usuario=usuario.id))
   return render_template('criar_conta.html', form=form_criarconta)

@app.route('/perfil/<id_usuario>', methods=["POST", "GET"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # O usuário está acessando o próprio perfil
        form_foto = FormFoto()
        print(f"Método de requisição: {request.method}") # Debug: verificar se é POST
        print(f"Formulário recebido? {form_foto.foto.data}") # Debug: verifica se o arquivo está chegando
        if form_foto.validate_on_submit():
            print ("Formulário validado!")  # 🔹 Confirma se o formulário foi validado corretamente
            if not form_foto.validate_on_submit():
                print ("Formulário não validado!")  # 🔹 Confirma se o formulário não foi validado corretamente
                print (form_foto.errors)  # 🔹 Mostra os erros de validação do formulário
                return render_template('perfil.html', usuario=current_user, form=form_foto)
            arquivo = form_foto.foto.data
            print(f"Arquivo recebido: {arquivo}")  # 🔹 Verifica se o arquivo foi recebido corretamente
            
            nome_seguro = secure_filename(arquivo.filename)
            print(f"Nome seguro do arquivo: {nome_seguro}")  # 🔹 Verifica se o nome do arquivo foi processado corretamente
            
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro)
            print(f"Caminho para salvar: {caminho}")  # 🔹 Mostra o caminho onde a imagem será salva
            
            arquivo.save(caminho)  # 🔹 Salva o arquivo na pasta fotos_posts
            
            # Registrar a foto no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            print("Foto salva no banco de dados!")  # 🔹 Confirma se a foto foi salva no banco

        return render_template('perfil.html', usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
   fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
   return render_template('feed.html', fotos=fotos)
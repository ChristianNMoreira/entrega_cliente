from flask import Blueprint, request, jsonify, render_template
from ..models import User
from ..extensions import db, mail, jwt
from flask_mail import Message
from flask_jwt_extended import jwt_required, create_access_token, decode_token, get_jwt_identity
import bcrypt

user_api = Blueprint('user_api', __name__)

@user_api.route('/users/', methods=['GET'])
def index():
    users = User.query.all()

    return jsonify([user.json() for user in users]), 200


@user_api.route('/users/', methods=['POST'])
def cadastro():
    data = request.json

    if not data:
        return {'erro': 'Request deve ter um body'}, 400

    name = data.get('name')
    email = data.get('email')
    idade = data.get('idade')
    password = data.get('password')

    test = User.query.filter_by(email=email).first()

    if test:
        return {'erro': 'email ja cadastrado'}, 400

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user = User(name=name, email=email, idade=idade, password_hash=password_hash)

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    
    msg = Message(sender='christian.moreira@poli.ufrj.br', recipients=[email], subject='Bem-vindo!', html=render_template('email.html', name=name, token=token))

    mail.send(msg)

    return user.json(), 200

@user_api.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    '''
    if not data or not email or not password:
        return{'erro': 'Dados insuficientes'}, 400

    user = User.query.filter_by(email=email).first

    if not user or not bcrypt.checkpw(password.encode(), user.password_hash):
        return{'erro': 'Dados invalidos'}, 400

    token = create_access_token(identify=user.id)

    return{'token': token}, 200
    '''
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'erro': 'Usuario ou senha incorretos'}, 400

    if not user.active:
        return {'erro': 'Usuario nao esta ativo'}, 400

    if bcrypt.checkpw(password.encode(), user.password_hash):
        access_token = create_access_token(identity=user.id)
        #return {'msg': 'Login completo!'}, 200
        return jsonify(access_token=access_token), 200

    else:
        return {'erro': 'Usuario ou senha incorretos'}, 400

@user_api.route('/users/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@jwt_required
def user_detail(id):
    user = User.query.get_or_404(id)

    current_user_id = get_jwt_identity()

    if current_user_id != id:
        return {'erro': 'Nao esta logado na sua conta'}, 400

    if request.method == 'GET':
        return user.json(), 200

    if request.method == 'PUT':
        data = request.json
        
        if not data:
            return {'erro': 'Request deve ter um body'}, 400

        name = data.get('name')
        email = data.get('email')
        idade = data.get('idade')

        if not name or not email:
            return {'erro': 'Dados devem ser preenchidos'}, 400
        
        test = User.query.filter_by(email=email).first()

        if test and email != user.email:
            return {'erro': 'email ja cadastrado'}, 400

        user.name = name
        user.email = email
        user.idade = idade

        db.session.add(user)
        db.session.commit()

        return user.json(), 200

    if request.method == 'PATCH':
        data = request.json
        
        if not data:
            return {'erro': 'Request deve ter um body'}, 400

        email = data.get('email')
        
        test = User.query.filter_by(email=email).first()

        if test and email != user.email:
            return {'erro': 'email ja cadastrado'}, 400

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.idade = data.get('idade', user.idade)

        db.session.add(user)
        db.session.commit()

        return user.json(), 200

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {'msg': 'Usuario deletado'}, 200

@user_api.route('/users/activate/<token>', methods=['GET'])
def activate(token):
    data = decode_token(token)

    user = User.query.get_or_404(data['identity'])

    if user.active == False:
        user.active = True
        db.session.add(user)
        db.session.commit()

    return render_template('email2.html')

@user_api.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    #print(type(current_user))
    return jsonify(logged_in_as=current_user), 200
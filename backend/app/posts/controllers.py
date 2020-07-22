from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
#from datetime import datetime
from ..models import User, Post
from ..extensions import db

post_api = Blueprint('post_api', __name__)

##############
@post_api.route('/users/<int:id>/posts/', methods=['GET'])
def get_posts(id):
    user = User.query.get_or_404(id)
    posts = Post.query.filter_by(owner_id=id)
    return jsonify([post.json() for post in posts]), 200

#####################
@post_api.route('/users/<int:id>/posts/', methods=['POST'])
@jwt_required
def create(id):
    owner = User.query.get_or_404(id)

    current_user_id = get_jwt_identity()

    if current_user_id != id:
        return {'erro', 'Nao esta logado na sua conta'}, 400

    data = request.json

    text = data.get('text')
    img = data.get('img')

    if not data:
        return {'erro': 'Dados insuficienes'}, 400
    
    if not text and not img:
        return {'erro': 'Dados insuficienes'}, 400
    '''
    now = datetime.now()
    date_string = now.strftime("%m/%d/%Y, %H:%M:%S")
    '''
    post = Post(text=text, img=img, owner_id=owner.id)

    db.session.add(post)
    db.session.commit()

    return post.json(), 201

#MUDAR DELETE!
@post_api.route('/users/posts/', methods=['GET', 'DELETE'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return jsonify([post.json() for post in posts]), 200

    if request.method == 'DELETE':
        posts = Post.query.all()
        for post in posts:
            db.session.delete(post)
            db.session.commit()
        return {'msg': 'Posts deletados'}, 200

#######
@post_api.route('/users/posts/<int:id>', methods=['GET'])
def post_detail(id):
    post = Post.query.get_or_404(id)
    return post.json(), 200
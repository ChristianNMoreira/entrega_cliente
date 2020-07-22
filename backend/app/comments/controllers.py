from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
#from datetime import datetime
from ..models import User, Post, Comment
from ..extensions import db

comment_api = Blueprint('comment_api', __name__)

####################
@comment_api.route('/posts/<int:id>/comments/', methods=['POST'])
@jwt_required
def comment(id):
    post = Post.query.get_or_404(id)
    user_id = get_jwt_identity()

    data = request.json

    text = data.get('text')

    if not data or not text:
        return {'erro': 'Dados insuficienes'}, 400
    '''
    now = datetime.now()
    date_string = now.strftime("%m/%d/%Y, %H:%M:%S")
    '''
    comment = Comment(text=text, owner_id=id, user_id=user_id)

    db.session.add(comment)
    db.session.commit()

    return comment.json(), 201

@comment_api.route('/posts/<int:id>/comments/', methods=['GET'])
def get_comments(id):
    post = Post.query.get_or_404(id)
    comments = Comment.query.filter_by(owner_id=id)
    return jsonify([comment.json() for comment in comments]), 200
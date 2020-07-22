from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Chat, Message
from ..extensions import db

chat_api = Blueprint('chat_api', __name__)

@chat_api.route('/chats/', methods=['POST'])
@jwt_required
def create():
    data = request.json
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')

    test = Chat.query.filter_by(user1_id=user1_id, user2_id=user2_id).first()

    if test:
        return {'erro': 'Chat já existe'}, 400

    test = Chat.query.filter_by(user1_id=user2_id, user2_id=user1_id).first()

    if test:
        return {'erro': 'Chat já existe'}, 400

    chat = Chat(user1_id=user1_id, user2_id=user2_id)

    db.session.add(chat)
    db.session.commit()

    return chat.json(), 201
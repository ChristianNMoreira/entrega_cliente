from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Chat, Message
from ..extensions import db

message_api = Blueprint('message_api', __name__)

@message_api.route('/chats/<int:id>/messages/', methods=['GET', 'POST'])
@jwt_required
def message(id):
    chat = Chat.query.get_or_404(id)
    sender_id = get_jwt_identity()

    if request.method == 'GET':
        if sender_id != chat.user1_id and sender_id != chat.user2_id:
            return {'erro', 'Não autorizado'}, 400

        test = Message.query.filter_by(owner_id=id).first()
        if not test:
            return {'msg': 'nenhuma mensagem enviada'}, 200

        messages = Message.query.filter_by(owner_id=id)
        
        return jsonify([message.json() for message in messages]), 200

    if request.method == 'POST':
        user1 = User.query.get_or_404(chat.user1_id)
        user2 = User.query.get_or_404(chat.user2_id)
        
        if sender_id == chat.user1_id:
            receiver_id = chat.user2_id
            receiver_name = user2.name
            sender_name = user1.name

        if sender_id == chat.user2_id:
            receiver_id = chat.user1_id
            receiver_name = user1.name
            sender_name = user2.name

        data = request.json

        text = data.get('text')

        if not data or not text:
            return {'erro': 'Dados insuficienes'}, 400
        
        message = Message(text=text, owner_id=id, sender_id=sender_id, sender_name=sender_name, receiver_id=receiver_id, receiver_name=receiver_name)

        db.session.add(message)
        db.session.commit()

        return message.json(), 201
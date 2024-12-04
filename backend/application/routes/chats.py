from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_accepted

from application.setup.models import db, Chats, AdRequests
from application.setup.functions import ownership_required
from application.setup.errors import UserNotFoundError, UserAlreadyExists, ResourceNotFoundError, ResourceAlreadyExists, BadRequest, OwnershipRequired, InternalServerError


chat = Blueprint('chats', __name__)


@chat.get('/fetch')
@auth_required('token')
@roles_accepted('Sponsor', 'Admin', 'Influencer')
def get_chats(reqId):
    # retrive rows from charts table in asending order based on time colomn using AdRequests table
    chats = Chats.query.filter_by(adRequest_id = reqId).order_by(Chats.time.asc()).all()
    try:
        db_data = []
        for chat in chats:
            db_data.append({
                'id': chat.id,
                'commenter_id': chat.commenter_id,
                'commenter_role': chat.commenter,
                'comment': chat.comment,
                'time': chat.time,
                'request_id': chat.adRequest_id
            })
        
        return jsonify({'db_data': db_data,
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        raise InternalServerError(error_message=str(e))        


@chat.post('/create')
@auth_required('token')
@roles_accepted('Sponsor', 'Admin', 'Influencer')
def create_chat(reqId):
    obj = request.get_json()
    comment = obj.get('comment')

    if not comment:
        raise BadRequest(error_message='Missing required field')
    
    AdRequest = AdRequests.query.get(reqId)
    if AdRequest:
        try:
            chat = Chats(comment, reqId)
            db.session.add(chat)
            db.session.commit()

            db_data = {
                'id': chat.id,
                'commenter_id': chat.commenter_id,
                'commenter_role': chat.commenter,
                'comment': chat.comment,
                'time': chat.time,
                'request_id': chat.adRequest_id,
            }

            return jsonify({'db_data': db_data,
                            'code'   : 'SUCCESS',
                            'message': 'Operations completed successfully'}), 200
        except Exception as e:
            raise InternalServerError(error_message=str(e))        
    else:
        raise ResourceNotFoundError(error_message='AdRequest not found')



@chat.put('/edit/<int:chat_id>')
@auth_required('token')
@roles_accepted('Sponsor', 'Admin', 'Influencer')
@ownership_required
def update_chat(chat_id):
    obj = request.get_json()
    comment = obj.get('comment')

    if not comment:
        raise BadRequest(error_message='Missing required field')
    
    chat = Chats.query.get(chat_id)
    if chat:
        try:
            chat.comment = comment
            db.session.commit()
            return jsonify({'db_data': {},
                            'code'   : 'SUCCESS',
                            'message': 'Operations completed successfully'}), 200
        except Exception as e:
            raise InternalServerError(error_message=str(e))        
    else:
        raise ResourceNotFoundError(error_message='Chats not found')



@chat.delete('/delete/<int:chat_id>')
@auth_required('token')
@roles_accepted('Sponsor', 'Admin', 'Influencer')
@ownership_required
def delete_chat(chat_id):
    chat = Chats.query.get(chat_id)
    if chat:
        try:
            db.session.delete(chat)
            db.session.commit()
            return jsonify({'db_data': {},
                            'code'   : 'SUCCESS',
                            'message': 'Operations completed successfully'}), 200
        except Exception as e:
            raise InternalServerError(error_message=str(e))        
    else:
        raise ResourceNotFoundError(error_message='Chats not found')
    

    
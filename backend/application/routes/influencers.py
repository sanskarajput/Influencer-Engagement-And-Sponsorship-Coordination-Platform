from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, roles_accepted
import base64

from application.setup.models import db, Users , Influencers
from application.setup.functions import ownership_required
from application.setup.errors import UserNotFoundError, ResourceNotFoundError, BadRequest, InternalServerError

import imghdr

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(file):
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


influ = Blueprint('influencers', __name__)


@influ.route('/influencer-details/<int:user_id>')
@auth_required('token')
@roles_accepted('Influencer','Sponsor','Admin')
def influencers_details(user_id):
    user = Users.query.get(user_id)
    if not user:
        raise UserNotFoundError()
    
    influencer = user.influencer_details
    if not influencer:
        raise UserNotFoundError(error_message='Logged in user (Influencer) is not authorized to view this resource OR may not EXIST.', error_code='UNAUTHORIZED')
    
    try:
        db_data = {'influencer_id':influencer.id,
                   'category':influencer.category,
                   'niche':influencer.niche,
                   'reach': influencer.reach,
                   'description':influencer.description,
                   'link':influencer.link,
                   'isActive':influencer.user.is_active,
                   'influencer_s_user_id':influencer.user.id,
                   'username':influencer.user.username,
                   'email':influencer.user.email,
                   'name':influencer.user.name,
                   'avatar':base64.b64encode(influencer.user.avatar).decode('utf-8') if influencer.user.avatar else influencer.user.avatar,
                   'time':influencer.user.time}
        
        return jsonify({'db_data': db_data,
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200

    except:
        raise InternalServerError(error_message='While parseing json some error occurred')
        


@influ.patch('/edit-influencer-username/<int:user_id>')
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_username(user_id):
    obj = request.get_json()
    username = obj.get('username')

    if not username:
        raise BadRequest(error_message='Missing required field')
    
    # first check is this given username will be unique in that username column
    is_user = Users.query.filter_by(username=username).first()
    if is_user:
        raise BadRequest(error_message='Username already exist')
    
    user = Users.query.get(user_id)
    if not user:
        raise ResourceNotFoundError(error_message='Influencer not found')
    
    try:
        user.username = username
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@influ.patch('/edit-influencer-name/<int:user_id>')
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_name(user_id):
    obj = request.get_json()
    name = obj.get('name')

    if not name:
        raise BadRequest(error_message='Missing required field')
    
    user = Users.query.get(user_id)
    if not user:
        raise UserNotFoundError()
    
    try:
        user.name = name
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    


@influ.patch('/edit-influencer-avatar/<int:user_id>')
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_avatar(user_id):
    if 'avatar' not in request.files:
        raise BadRequest(error_message='Missing required file')

    file = request.files['avatar']

    if not file or file.filename == '':
        raise BadRequest(error_message='Invalid file provided')
    
    if not allowed_file(file) or imghdr.what(file) not in ALLOWED_EXTENSIONS:
        raise BadRequest(error_message='Invalid file format')

    user = Users.query.get(user_id)
    if not user:
        raise UserNotFoundError()

    try:
        user.avatar = file.read()  # Read binary data
        db.session.commit()

        return jsonify({
            'db_data': {},
            'code': 'SUCCESS',
            'message': 'Avatar updated successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@influ.delete('/delete-influencer-avatar/<int:user_id>')
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def delete_influencers_avatar(user_id):
    user = Users.query.get(user_id)
    if not user:
        raise UserNotFoundError()
    
    try:
        user.avatar = None
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@influ.route('/edit-influencer-category/<int:influencer_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_category(influencer_id):
    obj = request.get_json()

    if 'category' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    influencer = Influencers.query.get(influencer_id)
    if not influencer:
         raise ResourceNotFoundError(error_message='Influencer not found')
    
    try:
        influencer.category = obj.get('category')
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))        
        


@influ.route('/edit-influencer-niche/<int:influencer_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_niche(influencer_id):
    obj = request.get_json()

    if 'niche' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    influencer = Influencers.query.get(influencer_id)
    if not influencer:
         raise ResourceNotFoundError(error_message='Influencer not found')
    
    try:
        influencer.niche = obj.get('niche')
        db.session.commit()   
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))        



@influ.route('/edit-influencer-reach/<int:influencer_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_reach(influencer_id):
    obj = request.get_json()
        
    if 'reach' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    influencer = Influencers.query.get(influencer_id)
    if not influencer:
         raise ResourceNotFoundError(error_message='Influencer not found')
    
    
    try:
        influencer.reach = int(obj.get('reach'))
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except ValueError as e:
        raise BadRequest(error_message='Reach must be a positive integer')
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))        

    

@influ.route('/edit-influencer-description/<int:influencer_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_description(influencer_id):
    obj = request.get_json()

    if 'description' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    influencer = Influencers.query.get(influencer_id)
    if not influencer:
         raise ResourceNotFoundError(error_message='Influencer not found')
    
    try:
        influencer.description = obj.get('description')
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))        



@influ.route('/edit-influencer-link/<int:influencer_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Influencer')
@ownership_required
def edit_influencers_link(influencer_id):
    obj = request.get_json()

    if 'link' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    influencer = Influencers.query.get(influencer_id)
    if not influencer:
         raise ResourceNotFoundError(error_message='Influencer not found')
    
    try:
        influencer.link = obj.get('link')
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))    


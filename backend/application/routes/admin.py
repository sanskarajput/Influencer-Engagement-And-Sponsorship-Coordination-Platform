from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, roles_accepted
from application.setup.models import db, Users , Sponsors 

from application.setup.functions import ownership_required
from application.setup.errors import UserNotFoundError, BadRequest, InternalServerError
import base64

import imghdr

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(file):
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




admin = Blueprint('Admin', __name__)

@admin.route('/admin-details/<int:user_id>')
@auth_required('token')
@roles_accepted('Admin')
def admin_details(user_id):
    user = Users.query.get(user_id)
    if not user:
        raise UserNotFoundError()
    
    try:
        db_data = {'user_id':user.id,
                   'username':user.username,
                   'email':user.email,
                   'name':user.name,
                   'avatar':base64.b64encode(user.avatar).decode('utf-8') if user.avatar else user.avatar,
                   'time':user.time}
        
        return jsonify({'db_data': db_data,
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except:
        raise InternalServerError(error_message='While parseing json some error occurred')
    


@admin.patch('/edit-admin-username/<int:user_id>')
@auth_required('token')
@roles_required('Admin')
@ownership_required
def edit_admin_username(user_id):
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
        raise UserNotFoundError()
    
    try:
        user.username = username
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@admin.patch('/edit-admin-name/<int:user_id>')
@auth_required('token')
@roles_required('Admin')
@ownership_required
def edit_admin_name(user_id):
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
    


@admin.patch('/edit-admin-avatar/<int:user_id>')
@auth_required('token')
@roles_required('Admin')
@ownership_required
def edit_admin_avatar(user_id):
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
        # Save binary content to the database
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



@admin.delete('/delete-admin-avatar/<int:user_id>')
@auth_required('token')
@roles_required('Admin')
@ownership_required
def delete_admin_avatar(user_id):
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


from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, roles_accepted
from application.setup.models import db, Users , Sponsors 

from application.setup.functions import ownership_required
from application.setup.errors import UserNotFoundError, ResourceNotFoundError, BadRequest, InternalServerError
import base64

import imghdr

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(file):
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


spon = Blueprint('sponsors', __name__)


@spon.route('/sponsor-details/<int:user_id>')
@auth_required('token')
@roles_accepted('Sponsor','Influencer','Admin')
def sponsors_details(user_id):
    user = Users.query.get(user_id)
    if not user:
        raise UserNotFoundError()
    
    sponsor = user.sponsor_details
    if not sponsor:
        raise UserNotFoundError(error_message='Logged in user (Sponsor) is not authorized to view this resource OR may not EXIST.', error_code='UNAUTHORIZED')

    try:
        db_data = {'sponsor_id':sponsor.id,
                   'type':sponsor.typee,
                   'industry':sponsor.industry,
                   'budget': sponsor.budget,
                   'description':sponsor.description,
                   'isApproved':sponsor.approved,
                   'sponsor_s_user_id':sponsor.user.id,
                   'username':sponsor.user.username,
                   'email':sponsor.user.email,
                   'name':sponsor.user.name,
                   'avatar':base64.b64encode(sponsor.user.avatar).decode('utf-8') if sponsor.user.avatar else sponsor.user.avatar,
                   'time':sponsor.user.time}
        
        return jsonify({'db_data': db_data,
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except:
        raise InternalServerError(error_message='While parseing json some error occurred')



@spon.get('/sponsor/is-approved/<int:sponsor_id>')
@auth_required('token')
@roles_required('Sponsor')
def is_sponsor_approved(sponsor_id):
    sponsor = Sponsors.query.get(sponsor_id)
    if not sponsor:
        raise ResourceNotFoundError(error_message='Sponsor not found')

    try:
        return jsonify({'db_data': {'isApproved': (lambda sponsor: True if sponsor.approved == "TRUE" else False)(sponsor)},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except:
        raise InternalServerError(error_message='While parseing json some error occurred')



@spon.patch('/edit-sponsor-username/<int:user_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_sponsors_username(user_id):
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



@spon.patch('/edit-sponsor-name/<int:user_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_sponsors_name(user_id):
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
    


@spon.patch('/edit-sponsor-avatar/<int:user_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_sponsors_avatar(user_id):
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
    


@spon.delete('/delete-sponsor-avatar/<int:user_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def delete_sponsors_avatar(user_id):
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



@spon.route('/edit-sponsor-type/<int:sponsor_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_sponsors_type(sponsor_id):
    obj = request.get_json()

    if 'type' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    sponsor = Sponsors.query.get(sponsor_id)
    if not sponsor:
        raise ResourceNotFoundError(error_message='Sponsor not found')

    try:
        sponsor.typee = obj.get('type')
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@spon.route('/edit-sponsor-industry/<int:sponsor_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_sponsors_industry(sponsor_id):
    obj = request.get_json()

    if 'industry' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    sponsor = Sponsors.query.get(sponsor_id)
    if not sponsor:
        raise ResourceNotFoundError(error_message='Sponsor not found')
    
    try:
        sponsor.industry =  obj.get('industry')
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@spon.route('/edit-sponsor-budget/<int:sponsor_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_sponsors_budget(sponsor_id):
    obj = request.get_json()

    if 'budget' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    budget = obj.get('budget')
    # if budget is string or less than 0 then
    try:
        budget = float(budget)
        if budget < 0:
            raise BadRequest(error_message='Budget should be positive')
    except ValueError:
            raise BadRequest(error_message='Budget must be a number')
    
    sponsor = Sponsors.query.get(sponsor_id)
    if not sponsor:
        raise ResourceNotFoundError(error_message='Sponsor not found')
    
    try:
        sponsor.budget = budget
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@spon.route('/edit-sponsor-description/<int:sponsor_id>', methods = ['PATCH'])
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_sponsors_description(sponsor_id):
    obj = request.get_json()

    if 'description' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    sponsor = Sponsors.query.get(sponsor_id)
    if not sponsor:
        raise ResourceNotFoundError(error_message='Sponsor not found')

    try:
        sponsor.description = obj.get('description')
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))

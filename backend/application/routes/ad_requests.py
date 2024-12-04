from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_accepted, current_user

from application.setup.models import db, Influencers , Campaigns,  AdRequests, RequestStatus, Users

from application.setup.functions import ownership_required
from application.setup.errors import UserNotFoundError, UserAlreadyExists, ResourceNotFoundError, ResourceAlreadyExists, BadRequest, OwnershipRequired, InternalServerError


adRequest = Blueprint('ad_requests', __name__)



# will be remove because it snot for everyone
@adRequest.route('/<int:id>')
@auth_required('token')
@roles_accepted('Influencer','Sponsor','Admin')
def get_ad_requests(id):
    adRequest = AdRequests.query.get(id)
    if adRequest:
        try:
            db_data = {'id': adRequest.id,
                       'campaign_id': adRequest.campaign_id,
                       'influencer_id':adRequest.influencer_id,
                       'influencer_s_user_id':adRequest.influencer.user.id,
                       'message':adRequest.message,
                       'requirements':adRequest.requirements,
                       'payment':adRequest.payment,
                       'status':adRequest.status.name,
                       'time':adRequest.time,
                       'campaign_name':adRequest.campaign.name,
                       'influencer_name':adRequest.influencer.user.name}
                        
            return jsonify({'db_data': db_data,
                            'code'   : 'SUCCESS',
                            'message': 'Operations completed successfully'}), 200
        except Exception as e:
            raise InternalServerError(error_message='While parseing json some error occurred')
    else:
        raise ResourceNotFoundError(error_message='AdRequest not found')


@adRequest.post('/create')
@auth_required('token')
@roles_accepted('Sponsor')
def create_adRequest():
    obj = request.get_json()

    campaign_id = obj.get('campaign_id')
    influencer_s_user_id = obj.get('influencer_s_user_id')

    if not campaign_id or not influencer_s_user_id:
        raise BadRequest(error_message='Missing required field')

    campaign = Campaigns.query.get(campaign_id)
    if campaign is None:
        raise BadRequest(error_message='Campaign not found')
    
    user = Users.query.get(influencer_s_user_id)
    if user is None:
        raise BadRequest(error_message='User not found')
    
    influencer = user.influencer_details
    if not influencer:
        raise BadRequest(error_message='Influencer not found')
    
    influencer_id = influencer.id
    
    if current_user.roles == ['Sponsor'] and campaign.campaigner.user_id != current_user.id:
        raise BadRequest(error_message='Provided compaign_id is not yours')
    
    if current_user.roles == ['Influencer'] and influencer.user_id != current_user.id:
        raise BadRequest(error_message='Provided influencer_id is not yours')
    
    adRequest = AdRequests.query.filter_by(campaign_id = campaign_id, influencer_id = influencer_id).first()
    if adRequest:
        raise ResourceAlreadyExists(error_message='Add Request already exists')
    
    try:
        adRequest = AdRequests(campaign_id = campaign_id, influencer_id = influencer_id)
        db.session.add(adRequest)
        db.session.commit()

        db_data = {
            'influencer_s_user_id': adRequest.influencer.user.id,
            'influencer_username': adRequest.influencer.user.username,
            'influencer_id': adRequest.influencer.id,
            'influencer_category': adRequest.influencer.category,
            'requestExist': True,
            'adRequest_id': adRequest.id,
            'time': adRequest.time,
            'message': adRequest.message,
            'requirements': adRequest.requirements,
            'payment': adRequest.payment,
            'status': adRequest.status.name
        }

        return jsonify({'db_data': db_data,
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))


# Define a transition hierarchy: What statuses can transition to others
TRANSITIONS = {
    RequestStatus.PENDING: {RequestStatus.ACCEPTED, RequestStatus.DECLINED, RequestStatus.REJECTED},
    RequestStatus.ACCEPTED: {RequestStatus.COMPLETED},
    RequestStatus.DECLINED: {RequestStatus.REJECTED, RequestStatus.ACCEPTED},  # Declined can only be rejected
    RequestStatus.COMPLETED: set(),  # No transitions allowed from completed
    RequestStatus.REJECTED: set()   # No transitions allowed from rejected
}

@adRequest.patch('/edit-all')
@auth_required('token')
@roles_accepted('Sponsor')
@ownership_required
def edit_adrequest_all(adRequest_id):
    obj = request.get_json()
    message = obj.get('message')
    requirements = obj.get('requirements')
    payment = obj.get('payment')
    status = obj.get('status')

    if not message or not requirements or not payment or not status:
        raise BadRequest(error_message='Missing required field')
   
    try:
        payment = float(payment)
        if payment < 0:
            raise BadRequest(error_message='Payment should be positive')
    except ValueError:
            raise BadRequest(error_message='Payment must be a number')
    
    try:
        status = status.lower()
        if status not in RequestStatus.values:
            raise BadRequest(error_message='Invalid status. Status must be either Pending, Accepted, Completed, Declined or Rejected')
    except ValueError as e:
            raise BadRequest(error_message='Invalid status')
    
    adRequest = AdRequests.query.get(adRequest_id)
    if not adRequest:
        raise ResourceNotFoundError(error_message='AdRequest not found')

    allowed_transitions = [x.value for x in TRANSITIONS[adRequest.status]]
    if status not in allowed_transitions:
        raise BadRequest(error_message=f"Cannot update status from {adRequest.status.value} to {status}")
    
    try:
        adRequest.message = message
        adRequest.requirements = requirements
        adRequest.payment = payment
        adRequest.status = getattr(RequestStatus, status.upper(), None)
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))




@adRequest.patch('/edit-message/<int:adRequest_id>')
@auth_required('token')
@roles_accepted('Sponsor')
@ownership_required
def edit_adrequest_message(adRequest_id):
    obj = request.get_json()
    message = obj.get('message')

    if not message:
        raise BadRequest(error_message='Missing required field')
    
    adRequest = AdRequests.query.get(adRequest_id)
    if not adRequest:
        raise ResourceNotFoundError(error_message='AdRequest not found')
    
    try:
        adRequest.message = message
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    


@adRequest.patch('/edit-requirements/<int:adRequest_id>')
@auth_required('token')
@roles_accepted('Sponsor')
@ownership_required
def edit_adrequest_requirements(adRequest_id):
    obj = request.get_json()
    requirements = obj.get('requirements')

    if not requirements:
        raise BadRequest(error_message='Missing required field')
    
    adRequest = AdRequests.query.get(adRequest_id)
    if not adRequest:
        raise ResourceNotFoundError(error_message='AdRequest not found')
    
    try:
        adRequest.requirements = requirements
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    


@adRequest.patch('/edit-payment/<int:adRequest_id>')
@auth_required('token')
@roles_accepted('Sponsor')
@ownership_required
def edit_adrequest_payment(adRequest_id):
    obj = request.get_json()
    payment = obj.get('payment')

    if not payment:
        raise BadRequest(error_message='Missing required field')
    
    try:
        payment = float(payment)
        if payment < 0:
            raise BadRequest(error_message='Payment should be positive')
    except ValueError:
            raise BadRequest(error_message='Payment must be a number')
    
    
    adRequest = AdRequests.query.get(adRequest_id)
    if not adRequest:
        raise ResourceNotFoundError(error_message='AdRequest not found')
    
    try:
        adRequest.payment = payment
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    






@adRequest.patch('/edit-status/<int:adRequest_id>')
@auth_required('token')
@roles_accepted('Influencer','Sponsor')
@ownership_required
def edit_adrequest_status(adRequest_id):
    obj = request.get_json()
    status = obj.get('status')

    if not status:
        raise BadRequest(error_message='Missing required field')
    
    try:
        status = status.lower()
        if status not in RequestStatus.values:
            raise BadRequest(error_message='Invalid status. Status must be either Pending, Accepted, Completed, Declined or Rejected')
    except ValueError as e:
            raise BadRequest(error_message='Invalid status')
    
    adRequest = AdRequests.query.get(adRequest_id)
    if not adRequest:
        raise ResourceNotFoundError(error_message='AdRequest not found')

    allowed_transitions = [x.value for x in TRANSITIONS[adRequest.status]]
    if status not in allowed_transitions:
        raise BadRequest(error_message=f"Cannot update status from {adRequest.status.value} to {status}")

    try:
        adRequest.status = getattr(RequestStatus, status.upper(), None)
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@adRequest.delete('/delete/<int:adRequest_id>')
@auth_required('token')
@roles_accepted('Sponsor')
@ownership_required
def delete_adRequest(adRequest_id):
    adRequest = AdRequests.query.get(adRequest_id)
    if not adRequest:
        raise ResourceNotFoundError(error_message='AdRequest not found')
    
    try:
        db.session.delete(adRequest)
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))


















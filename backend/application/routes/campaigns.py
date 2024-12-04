from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user, roles_accepted
from datetime import datetime

from application.setup.models import db, Campaigns
from application.setup.functions import ownership_required , date_type, time_type
from application.setup.errors import UserNotFoundError, UserAlreadyExists, ResourceNotFoundError, ResourceAlreadyExists, BadRequest, OwnershipRequired, InternalServerError


campaign = Blueprint('campaigns', __name__)


@campaign.get('/<int:id>')
@auth_required('token')
@roles_accepted('Influencer','Sponsor','Admin')
def get_campaign(id):
    campaign = Campaigns.query.get(id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    try:
        db_data = {'id': campaign.id,
                   'name': campaign.name,
                   'description': campaign.description,
                   'category': campaign.category,
                   'start_date': campaign.start_date,
                   'end_date': campaign.end_date,
                   'budget': campaign.budget,
                   'flagged': campaign.flagged,
                   'visibility': campaign.visibility,
                   'goals': campaign.goals,
                   'time': campaign.time,
                   'campaigner': campaign.campaigner.user.username,
                   'campaigner_s_user_id': campaign.campaigner.user.id}
        
        return jsonify({'db_data':  db_data,
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except:
        raise InternalServerError(error_message='While parseing json some error occurred')
    

@campaign.post('/add-new')
@auth_required('token')
@roles_required('Sponsor')
def create_campaign():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    start_date = data.get('start_date')
    start_time = data.get('start_time')
    end_date = data.get('end_date')
    end_time = data.get('end_time')
    budget = data.get('budget')
    visibility = data.get('visibility')
    goals = data.get('goals')
    creater_id_which_is_a_sponsor = current_user.sponsor_details.id  
    # creater_id_which_is_a_sponsor = data.get('sponsor_id') 

    if not name or not description or not category or not start_date or not start_time or not end_date or not end_time or not budget or not visibility or not goals or not creater_id_which_is_a_sponsor:
        raise BadRequest(error_message='Missing required field')

    campaign = Campaigns.query.filter_by(creater_id_which_is_a_sponsor = current_user.sponsor_details.id, name = name).first()

    if campaign:
        raise ResourceAlreadyExists(error_message='Campaign already exists')
    
    start_date, end_date = date_type(start_date), date_type(end_date)
    start_time, end_time = time_type(start_time), time_type(end_time)

    try:
        budget = float(budget)
        if budget < 0:
            raise BadRequest(error_message='Budget must be positive')
    except ValueError:
        raise BadRequest(error_message='Budget must be a number')
    
    try:
        visibility = visibility.upper()
        if visibility not in ['PUBLIC', 'PRIVATE']:
            raise BadRequest(error_message='Invalid visibility')
    except ValueError:
        raise BadRequest(error_message='Visibility must be a string')

    try:
        start_date_time = datetime.combine(start_date, start_time)
        end_date_time = datetime.combine(end_date, end_time)

        if start_date_time >= end_date_time:
            raise BadRequest(error_message='End timing should be greater than Start timing')
        
        campaign = Campaigns(name = name,
                            description = description,
                            category = category,
                            start_date = start_date_time,
                            end_date = end_date_time,
                            budget = budget,
                            visibility = visibility,
                            goals = goals,
                            creater_id_which_is_a_sponsor = creater_id_which_is_a_sponsor
                            )

        db.session.add(campaign)
        db.session.commit()
        return jsonify({'db_data': { "id" : campaign.id },
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    
    except ValueError as e:
        # db.session.rollback() # no need
        raise InternalServerError(error_message=str(e))
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))


@campaign.route('/edit-all/<int:campaign_id>',methods=['GET', 'PUT']) 
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_all(campaign_id):
    if request.method == "GET":
        campaign = Campaigns.query.get(campaign_id)
        if not campaign:
            raise ResourceNotFoundError(error_message='Campaign not found')

        try:
            db_data = {'id': campaign.id,
                       'name': campaign.name,
                       'description': campaign.description,
                       'category': campaign.category,
                       'start_date': campaign.start_date,
                       'end_date': campaign.end_date,
                       'budget': campaign.budget,
                       'visibility': campaign.visibility,
                       'goals': campaign.goals,
                       'time': campaign.time,
                       'campaigner': campaign.campaigner.user.username,
                       'campaigner_s_user_id': campaign.campaigner.user.id}
        
            return jsonify({'db_data':  db_data,
                            'code'   : 'SUCCESS',
                            'message': 'Operations completed successfully'}), 200
        except:
            raise InternalServerError(error_message='While parseing json some error occurred')
        
    obj = request.get_json()
    name = obj.get('name')
    description = obj.get('description')
    category = obj.get('category')
    start_date = obj.get('start_date')
    start_time = obj.get('start_time')
    end_date = obj.get('end_date')
    end_time = obj.get('end_time')
    budget = obj.get('budget')
    visibility = obj.get('visibility')
    goals = obj.get('goals')

    if not name or not description or not category or not start_date or not start_time or not end_date or not end_time or not budget or not visibility or not goals:
        raise BadRequest(error_message='Missing required field')

    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')

    start_date, end_date = date_type(start_date), date_type(end_date)
    start_time, end_time = time_type(start_time), time_type(end_time)

    try:
        budget = float(budget)
        if budget < 0:
            raise BadRequest(error_message='Budget must be positive')
    except ValueError:
        raise BadRequest(error_message='Budget must be a number')
    
    try:
        visibility = visibility.upper()
        if visibility not in ['PUBLIC', 'PRIVATE']:
            raise BadRequest(error_message='Invalid visibility')
    except ValueError:
        raise BadRequest(error_message='Visibility must be a string')

    try:
        start_date_time = datetime.combine(start_date, start_time)
        end_date_time = datetime.combine(end_date, end_time)

        if start_date_time >= end_date_time:
            raise BadRequest(error_message='End timing should be greater than Start timing')
        
        campaign.name = name
        campaign.description = description
        campaign.category = category
        campaign.start_date = start_date_time
        campaign.end_date = end_date_time
        campaign.budget = budget
        campaign.visibility = visibility
        campaign.goals = goals
        db.session.commit()

        return jsonify({'db_data': { "id" : campaign.id },
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except ValueError as e:
        # db.session.rollback() # no need
        raise InternalServerError(error_message=str(e))
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    

@campaign.patch('/edit-name/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_name(campaign_id):
    obj = request.get_json()
    name = obj.get('name')

    if not name:
        raise BadRequest(error_message='Missing required field')

    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    campaign_exist_with_this_name = Campaigns.query.filter_by(creater_id_which_is_a_sponsor = campaign.creater_id_which_is_a_sponsor, name = name).first()
    if campaign_exist_with_this_name:
        raise ResourceAlreadyExists(error_message='Choose another campaign name')
    
    try:
        campaign.name = name
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@campaign.patch('/edit-description/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_description(campaign_id):
    obj = request.get_json()
    description = obj.get('description')

    if not description:
        raise BadRequest(error_message='Missing required field')

    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    try:
        campaign.description = description
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    

@campaign.patch('/edit-category/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_category(campaign_id):
    obj = request.get_json()
    category = obj.get('category')

    if not category:
        raise BadRequest(error_message='Missing required field')
    
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    try:
        campaign.category = category
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))


@campaign.patch('/edit-budget/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_budget(campaign_id):
    obj = request.get_json()
    budget = obj.get('budget')

    if not budget:
        raise BadRequest(error_message='Missing required field')
    
    # if budget is string or less than 0 then
    try:
        budget = float(budget)
        if budget < 0:
            raise BadRequest(error_message='budget must be positive')
    except ValueError:
        raise BadRequest(error_message='budget must be a number')
    
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    try:
        campaign.budget = budget
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    


@campaign.patch('/edit-visibility/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_visibility(campaign_id):
    obj = request.get_json()
    visibility = obj.get('visibility')

    if not visibility:
        raise BadRequest(error_message='Missing required field')
    
    try:
        visibility = visibility.upper()
        if visibility not in ['PUBLIC', 'PRIVATE']:
            raise BadRequest(error_message='Invalid visibility')
    except ValueError:
        raise BadRequest(error_message='Visibility must be a string')
    
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    try:
        campaign.visibility = visibility
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))
    
    

@campaign.patch('/edit-goals/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_goals(campaign_id):
    obj = request.get_json()
    goals = obj.get('goals')

    if not goals:
        raise BadRequest(error_message='Missing required field')
    
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')

    try:
        campaign.goals = goals
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))






################## can be incorrect
@campaign.patch('/edit-start-date/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_start_date(campaign_id):
    obj = request.get_json()
    start_date = obj.get('start_date')
    start_time = obj.get('start_time')

    if not start_date or not start_time:
        raise BadRequest(error_message='Missing required field')
    
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    start_date = date_type(start_date)
    start_time = time_type(start_time)

    start_date_time = datetime.combine(start_date, start_time)
    if start_date_time >= campaign.end_date:
            raise BadRequest(error_message='End timing should be greater than Start timing')
    
    try:
        campaign.start_date = start_date_time
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))


################## can be incorrect
@campaign.patch('/edit-end-date/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def edit_campaign_end_date(campaign_id):
    obj = request.get_json()
    end_date = obj.get('end_date')
    end_time = obj.get('end_time')

    if not end_date or not end_time:
        raise BadRequest(error_message='Missing required field')
    
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    end_date = date_type(end_date)
    end_time = time_type(end_time)

    try:
        end_date_time = datetime.combine(end_date, end_time)
        if end_date_time <= campaign.start_date:
            raise BadRequest(error_message='End timing should be greater than Start timing')
        
        campaign.end_date = end_date_time
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@campaign.delete('/delete/<int:campaign_id>')
@auth_required('token')
@roles_required('Sponsor')
@ownership_required
def delete_campaign(campaign_id):
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    try:
        db.session.delete(campaign)
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))











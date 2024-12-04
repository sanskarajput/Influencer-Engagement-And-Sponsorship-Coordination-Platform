from flask import Blueprint, request, jsonify, Response
from flask_security import auth_required, roles_accepted

from application.setup.models import db, AdRequests, Campaigns, Sponsors, Users, Influencers
from application.setup.errors import ResourceNotFoundError, BadRequest, InternalServerError
from sqlalchemy import asc, desc, case, and_, func
import time, base64
from datetime import datetime, timedelta

admin_resources = Blueprint('Admin-resources', __name__ )


@admin_resources.post('/sponsor-approval/<int:sponsor_id>')
@auth_required('token')
@roles_accepted('Admin')
def approve_sponsor(sponsor_id):
    obj = request.get_json()

    if 'status' not in obj:
        raise BadRequest(error_message='Missing required field')
    
    status = obj.get('status')

    if status not in ['TRUE', 'FALSE']:
        raise BadRequest(error_message='Invalid status')
    
    sponsor = Sponsors.query.get(sponsor_id)
    if not sponsor:
        raise ResourceNotFoundError(error_message='Sponsor not found')
    
    try:
        sponsor.approved = status
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@admin_resources.post('/toggle-campaign-flagged/<int:campaign_id>')
@auth_required('token')
@roles_accepted('Admin')
def campaign_flagged(campaign_id):
    campaign = Campaigns.query.get(campaign_id)

    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')
    
    try:
        campaign.flagged = not campaign.flagged
        db.session.commit()
        return jsonify({'db_data': {},
                        'code'   : 'SUCCESS',
                        'message': 'Operations completed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(error_message=str(e))



@admin_resources.get('/admin-dashboard-details')
@auth_required('token')
@roles_accepted('Admin')
def admin_dashboard_details():
    """
    """
    ####################################################################################################
    total_influencers = db.session.query(
        func.count(Influencers.id).label('total_influencers')
    ).scalar()
    ####################################################################################################


    ####################################################################################################
    total_sponsors = db.session.query(
        func.count(Sponsors.id).label('total_sponsors')
    ).scalar()
    ####################################################################################################


    ####################################################################################################
    total_campaigns = db.session.query(
        func.count(Campaigns.id).label('total_campaigns')
    ).scalar()
    ####################################################################################################


    ####################################################################################################
    total_requests = db.session.query(
        func.count(AdRequests.id).label('total_requests')
    ).scalar()
    ####################################################################################################


    ####################################################################################################
    total_pending_requests = db.session.query(
        func.count(AdRequests.id).label('total_pending_requests')
    ).filter(
        AdRequests.status == 'PENDING',
    ).scalar()
    ####################################################################################################


    ####################################################################################################
    total_completed_requests = db.session.query(
        func.count(AdRequests.id).label('total_completed_requests')
    ).filter(
        AdRequests.status == 'COMPLETED',
    ).scalar()
    ####################################################################################################


    ####################################################################################################
    utc_time = datetime.now()
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    
    total_active_campaigns = db.session.query(
        func.count(Campaigns.id).label('total_active_campaigns')
    ).filter(
        Campaigns.start_date <= ist_time, Campaigns.end_date >= ist_time
    ).scalar()
    ####################################################################################################



    ####################################################################################################
    campaigns_total_budget = db.session.query(
        func.sum(Campaigns.budget).label('campaigns_total_budget')
    ).scalar()
    ####################################################################################################




    ####################################################################################################
    # charts
    ####################################################################################################

    db_data = {
        'stats': {
            'total_influencers': total_influencers,
            'total_sponsors': total_sponsors,
            'total_campaigns': total_campaigns,
            'total_requests': total_requests,
            'total_pending_requests': total_pending_requests,
            'total_completed_requests': total_completed_requests,
            'total_active_campaigns': total_active_campaigns,
            'campaigns_total_budget': campaigns_total_budget,
        },
        'charts' :{

        }
    }

    return jsonify({'db_data': db_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@admin_resources.get('/all-campaigns-for-a-Admin')
@auth_required('token')
@roles_accepted('Admin')
def all_campaigns_for_admin():
    # Extract request parameters
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', '')
    search_on = request.args.get('searchOn', '')

    # Initial query to get the total number of records for the sponsor without filters
    base_query = db.session.query(
        Campaigns.id.label('id'),
        Campaigns.name.label('name'),
        Campaigns.description.label('description'),
        Campaigns.category.label('category'),
        Campaigns.flagged.label('flagged'),
        Campaigns.start_date.label('start_date'),
        Campaigns.end_date.label('end_date'),
        Campaigns.budget.label('budget'),
        Campaigns.visibility.label('visibility'),
        Campaigns.goals.label('goals'),
        Campaigns.time.label('time'),
        Users.username.label('sponsor_username'),
        Users.id.label('sponsor_s_user_id')
        ).join(Sponsors, Campaigns.creater_id_which_is_a_sponsor == Sponsors.id)\
         .join(Users, Sponsors.user_id == Users.id)
    
    records_total = base_query.count()

    # Build the query with search filter if provided
    query = base_query
    if search and search_on:
        columns_to_search = search_on.split(',')

        # print(columns_to_search)
        # Create search filters for each column
        search_filters = []
        for col in columns_to_search:
            if col == 'sponsor_username':
                search_filters.append(Users.username.ilike(f"%{search}%"))
            elif hasattr(Campaigns, col):  # Check if the column exists in the Campaigns model
                filter_condition = getattr(Campaigns, col).ilike(f"%{search}%")
                search_filters.append(filter_condition)
        
        # Apply OR filter for the search conditions
        if search_filters:  # Only apply if there are any filters
            query = query.filter(db.or_(*search_filters))

    # Count records after filtering
    records_filtered = query.count()

    # Apply sorting
    if hasattr(Campaigns, sort_by):
        sort_column = getattr(Campaigns, sort_by)
    elif sort_by == 'sponsor_username':
        sort_column = getattr(Users, 'username')
    else:
        sort_column = Campaigns.id

    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))
    # Apply pagination
    campaigns = query.offset(offset).limit(limit).all()

    # Format data for response
    campaigns_data = [
        {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'category': campaign.category,
            'flagged': campaign.flagged,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'time': campaign.time,
            'sponsor_username':campaign.sponsor_username,
            'sponsor_s_user_id':campaign.sponsor_s_user_id
        }
        for campaign in campaigns
    ]

    time.sleep(0.5)

    db_data = {
        "totalNotFiltered": records_total,       
        "total": records_filtered,  
        "rows": campaigns_data               
    }

    return jsonify({'db_data': db_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@admin_resources.get('/all-requests-with-this-campaign/<int:campaign_id>')
@auth_required('token')
@roles_accepted('Admin')
def all_requests_with_this_campaign(campaign_id):
    # retrivee campaign_category
    campaign = Campaigns.query.get(campaign_id)
    if not campaign:
        raise ResourceNotFoundError(error_message='Campaign not found')

    campaign_category = campaign.category

    base_query = db.session.query(
        Users.id.label('influencer_s_user_id'),
        Users.username.label('influencer_username'),
        Users.avatar.label('avatar'),
        Influencers.id.label("influencer_id"),
        Influencers.category.label("influencer_category"),
        case(
            (AdRequests.id.isnot(None), True),
            else_=False
        ).label('requestExist'),
        AdRequests.id.label('adRequest_id'),
        AdRequests.time,
        AdRequests.message,
        AdRequests.requirements,
        AdRequests.payment,
        AdRequests.status
    )\
     .join(AdRequests, 
               and_(
                   Influencers.id == AdRequests.influencer_id,
                   AdRequests.campaign_id == campaign_id
               ))\
    .join(Users, Users.id == Influencers.user_id)\
    .order_by(desc('requestExist'),
              case(
                (Influencers.category.like(f'%{campaign_category}%'), 0),
                else_=1
            ),
            Influencers.category.asc())
        
    influencer_request_data = [
        {
            'influencer_s_user_id': entry.influencer_s_user_id,
            'influencer_username': entry.influencer_username,
            'influencer_id': entry.influencer_id,
            'avatar': base64.b64encode(entry.avatar).decode('utf-8') if entry.avatar else entry.avatar,
            'influencer_category': entry.influencer_category,
            'requestExist': entry.requestExist,
            'adRequest_id': entry.adRequest_id,
            'time': entry.time,
            'message': entry.message,
            'requirements': entry.requirements,
            'payment': entry.payment,
            'status': entry.status.name if entry.status else entry.status
        }
        for entry in base_query.all()
    ]

    return jsonify({'db_data': influencer_request_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@admin_resources.get('/sponsor-approval-requests')
@auth_required('token')
@roles_accepted('Admin')
def sponsor_approval_requests():
    base_query = db.session.query(
        Sponsors.id.label('sponsor_id'),
        Sponsors.typee.label('type'),
        Sponsors.industry.label('industry'),
        Sponsors.budget.label('budget'),
        Sponsors.description.label('description'),
        Sponsors.approved.label('approved'),
        Users.id.label('sponsor_s_user_id'),
        Users.username.label('username'),
        Users.name.label('name'),
        Users.email.label('email'),
        Users.avatar.label('avatar'),
        Users.time.label('time'),
    ).join(Users, Users.id == Sponsors.user_id)\
     .filter(Sponsors.approved == 'PENDING')

    all_pending_approval = base_query.all()
    
    db_data = [
        {
            'sponsor_s_user_id': user.sponsor_s_user_id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'avatar': base64.b64encode(user.avatar).decode('utf-8') if user.avatar else user.avatar,
            'time': user.time,
            'sponsor_id': user.sponsor_id,
            'type': user.type,
            'industry': user.industry,
            'budget': user.budget,
            'description': user.description,
            'approved': user.approved,
        } 
        for user in all_pending_approval
    ]

    return jsonify({'db_data': db_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



from application.setup.celery.task import create_csv

@admin_resources.get('/csv-export')
@auth_required('token')
@roles_accepted('Admin')
def start_export():
    task = create_csv.apply_async()

     # Wait for the task to complete
    task_result = task.get(timeout=30)  # Adjust timeout as needed

    if task_result:
        # Return the CSV data as a downloadable file
        return Response(
            task_result,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=campaigns.csv"}
        )
    else:
        return jsonify({'error': 'Failed to generate CSV'}), 500


from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_accepted, current_user

from application.setup.models import db, Chats, AdRequests, Campaigns, Sponsors, Users, Influencers
from application.setup.functions import safe_get
from datetime import datetime, timedelta
from sqlalchemy import asc, desc, case, and_, func
import time, base64, calendar

influencer_resources = Blueprint('Influencer-resources', __name__ )

@influencer_resources.get('/influencer-dashboard-details')
@auth_required('token')
@roles_accepted('Influencer')
def influencer_dashboard_details():
    """
    1. total Requests : count 
    2. Total pending requests : count
    3. Earnings in current month : budget's sum 
    4. Earnings in current year : budget's sum 
    """
    ####################################################################################################
    total_requests = db.session.query(
        func.count(AdRequests.id).label('requests_count')
   ).filter(
        AdRequests.influencer_id == current_user.influencer_details.id
    ).scalar()
    ####################################################################################################





    ####################################################################################################
    total_pending_requests = db.session.query(
        func.count(AdRequests.id).label('pending_request_count')
    ).filter(
        AdRequests.status == 'PENDING',
        AdRequests.influencer_id == current_user.influencer_details.id
    ).scalar()
    ####################################################################################################




    ####################################################################################################
    current_year = datetime.now().year
    current_month = datetime.now().month
    # Get the first and last days of the current month
    first_day_of_month = datetime(current_year, current_month, 1)
    last_day_of_month = datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1])
    # Query AdRequests within the current month
    current_month_result = db.session.query(
        func.sum(AdRequests.payment).label('total_earnings'),
        func.count(AdRequests.id).label('request_count')
    ).filter(
        AdRequests.time.between(first_day_of_month, last_day_of_month),
        AdRequests.influencer_id == current_user.influencer_details.id 
    ).one_or_none()
    ####################################################################################################



    ####################################################################################################
    current_year = datetime.now().year
    # Get the first day and last day of the current year
    first_day_of_year = datetime(current_year, 1, 1)
    last_day_of_year = datetime(current_year, 12, 31)
    # Query to get both the sum of payment and the count of AdRequests
    current_year_result = db.session.query(
        func.sum(AdRequests.payment).label('total_earnings'),
        func.count(AdRequests.id).label('request_count'),
    ).filter(
        AdRequests.time.between(first_day_of_year, last_day_of_year),
        AdRequests.influencer_id == current_user.influencer_details.id  
    ).one_or_none()
    ####################################################################################################




    ####################################################################################################
    # charts
    ####################################################################################################

    db_data = {
        'stats': {
            'total_requests': total_requests,
            'total_pending_requests': total_pending_requests,
            'current_month': {
                'earnings':current_month_result.total_earnings or 0,
                'request_count' : current_month_result.request_count
            },
            'current_year': {
                'earnings': current_year_result.total_earnings or 0,
                'request_count' : current_year_result.request_count
            }
        },
        'charts' :{

        }
    }

    return jsonify({'db_data': db_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@influencer_resources.get('/search-by-influencers')
@auth_required('token')
@roles_accepted('Influencer')
def search_by_influencers():
    # ongoing campaigns (which are public), according to category, budget etc. and accept the request.
    query = request.args.get('query', '')
    queryList = query.lower().split(' ')

    # get time in (UTC)
    utc_time = datetime.now()
    # Manually adjust for IST (UTC + 5:30)
    ist_time = utc_time + timedelta(hours=5, minutes=30)

    base_query = db.session.query(
        Campaigns.id.label('campaign_id'),
        Campaigns.name.label('name'),
        Campaigns.description.label('description'),
        Campaigns.category.label('category'),
        Campaigns.start_date.label('start_date'),
        Campaigns.end_date.label('end_date'),
        Campaigns.budget.label('budget'),
        Campaigns.flagged.label('flagged'),
        Campaigns.visibility.label('visibility'),
        Campaigns.goals.label('goals'),
        Campaigns.time.label('time')
    ).filter(Campaigns.visibility == 'PUBLIC',Campaigns.start_date <= ist_time, Campaigns.end_date >= ist_time)

    search_filters = []
    if 'name' in queryList:
        parameter = safe_get(queryList,queryList.index('name')+1)
        search_filters.append(Campaigns.name.ilike(f"%{parameter}%"))
    if 'category' in queryList:
        parameter = safe_get(queryList,queryList.index('category')+1)
        search_filters.append(Campaigns.category.ilike(f"%{parameter}%"))
    if 'budget' in queryList:
        parameter = safe_get(queryList, queryList.index('budget') + 1)
        if parameter:
            try:
                budget_value = float(parameter)
                search_filters.append(Campaigns.budget == budget_value)
            except ValueError:
                pass
    if 'goals' in queryList:
        parameter = safe_get(queryList,queryList.index('goals')+1)
        search_filters.append(Campaigns.goals.ilike(f"%{parameter}%"))

    if search_filters:
        base_query = base_query.filter(db.or_(*search_filters))
    else:
        base_query = base_query.filter(Campaigns.description.ilike(f"%{query}%"))

    all_campaigns = base_query.all()
    
    campaigns_data = [
        {
            'campaign_id': campaign.campaign_id,
            'title': campaign.name,
            'description': campaign.description,
            'category': campaign.category,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'flagged': campaign.flagged,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'time': campaign.time
        } for campaign in all_campaigns
    ]

    return jsonify({'db_data': campaigns_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@influencer_resources.get('/all-public-campaigns')
@auth_required('token')
@roles_accepted('Influencer')
def all_public_campaigns():
    # get time in (UTC)
    utc_time = datetime.now()
    # Manually adjust for IST (UTC + 5:30)
    ist_time = utc_time + timedelta(hours=5, minutes=30)

    base_query = db.session.query(
        Campaigns.id.label('campaign_id'),
        Campaigns.name.label('name'),
        Campaigns.description.label('description'),
        Campaigns.category.label('category'),
        Campaigns.start_date.label('start_date'),
        Campaigns.end_date.label('end_date'),
        Campaigns.budget.label('budget'),
        Campaigns.flagged.label('flagged'),
        Campaigns.visibility.label('visibility'),
        Campaigns.goals.label('goals'),
        Campaigns.time.label('time')
    ).filter(Campaigns.visibility == 'PUBLIC',Campaigns.start_date <= ist_time, Campaigns.end_date >= ist_time)

    all_campaigns = base_query.all()
    
    campaigns_data = [
        {
            'campaign_id': campaign.campaign_id,
            'title': campaign.name,
            'description': campaign.description,
            'category': campaign.category,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'flagged': campaign.flagged,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'time': campaign.time
        } for campaign in all_campaigns
    ]

    return jsonify({'db_data': campaigns_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@influencer_resources.get('/all-requests-of-a-influencer')
@auth_required('token')
@roles_accepted('Influencer')
def all_requests_of_an_influencer():
    # Extract request parameters
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', '')
    search_on = request.args.get('searchOn', '')

    # Get the current influencer's ID
    influencer_id = current_user.influencer_details.id

    # Query to retrieve ad requests with related campaign and sponsor details
    base_query = db.session.query(
        AdRequests.id,
        AdRequests.message,
        AdRequests.requirements,
        AdRequests.payment,
        AdRequests.status,
        AdRequests.time,
        Campaigns.id.label('campaign_id'),
        Campaigns.name.label('campaign_name'),
        Users.id.label('sponsor_s_user_id'),
        Users.username.label('sponsor_username')
    ).join(Campaigns, AdRequests.campaign_id == Campaigns.id) \
    .join(Sponsors, Campaigns.creater_id_which_is_a_sponsor == Sponsors.id) \
    .join(Users, Sponsors.user_id == Users.id) \
    .filter(AdRequests.influencer_id == influencer_id)

    # Add search functionality if provided
    if search and search_on:
        columns_to_search = search_on.split(',')
        search_filters = []
        for col in columns_to_search:
            if col == 'campaign_name':
                search_filters.append(Campaigns.name.ilike(f"%{search}%"))
            elif col == 'sponsor_username':
                search_filters.append(Users.username.ilike(f"%{search}%"))
            elif hasattr(AdRequests, col):  # Check if the column exists in the AdRequests model
                filter_condition = getattr(AdRequests, col).ilike(f"%{search}%")
                search_filters.append(filter_condition)

        if search_filters:
            base_query = base_query.filter(db.or_(*search_filters))

    # Count records after filtering
    records_total = base_query.count()

    # Apply sorting
    if hasattr(AdRequests, sort_by):
        sort_column = getattr(AdRequests, sort_by)
    elif sort_by == 'campaign_name':
        sort_column = getattr(Campaigns, 'name')
    elif sort_by == 'sponsor_username':
        sort_column = getattr(Users, 'username')
    else:
        sort_column = AdRequests.id

    base_query = base_query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))

    # Apply pagination
    ad_requests = base_query.offset(offset).limit(limit).all()

    # Format data for response
    requests_data = [
        {
            'id': ad_request.id,
            'campaign_id': ad_request.campaign_id,
            'campaign_name': ad_request.campaign_name,
            'sponsor_s_user_id': ad_request.sponsor_s_user_id,
            'sponsor_username': ad_request.sponsor_username,
            'message': ad_request.message,
            'requirements': ad_request.requirements,
            'payment': ad_request.payment,
            'status': ad_request.status.name,  # Assuming you want to show the status name
            'time': ad_request.time
        }
        for ad_request in ad_requests
    ]

    db_data = {
        "totalNotFiltered": records_total,
        "total": len(requests_data),
        "rows": requests_data
    }

    return jsonify({'db_data': db_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@influencer_resources.get('/all-sponsors-profiles')
@auth_required('token')
@roles_accepted('Influencer','Admin')
def all_sponsors():
    sponsors = Sponsors.query.all()

    sponsors_data = [   
        {
            'sponsor_id':sponsor.id,
            'type':sponsor.typee,
            'industry':sponsor.industry,
            'budget': sponsor.budget,
            'description':sponsor.description,
            'sponsor_s_user_id':sponsor.user.id,
            'username':sponsor.user.username,
            'name':sponsor.user.name,
            'avatar':base64.b64encode(sponsor.user.avatar).decode('utf-8') if sponsor.user.avatar else sponsor.user.avatar,
            # 'isActive':sponsor.user.is_active,
            'isApproved':sponsor.approved
        }
        for sponsor in sponsors
    ]

    return jsonify({'db_data': sponsors_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@influencer_resources.get('/request-with-this-campaign/<int:campaign_id>/<int:influencer_id>')
@auth_required('token')
@roles_accepted('Influencer')
def request_with_this_campaign(campaign_id, influencer_id):
    # Get the current influencer's ID
    influencer_id = current_user.influencer_details.id

    ad_request = db.session.query(AdRequests).filter_by(campaign_id=campaign_id,influencer_id=influencer_id).first()

    requests_data = [
        {
            'adRequest_id': ad_request.id if ad_request else None,
            # 'campaign_id': ad_request.campaign_id if ad_request else None,
            # 'campaign_name': ad_request.campaign.name if ad_request else None,
            'sponsor_s_user_id': ad_request.campaign.campaigner.user.id if ad_request else None,
            'sponsor_username': ad_request.campaign.campaigner.user.username if ad_request else None,
            'avatar': (lambda ad_request: base64.b64encode(ad_request.campaign.campaigner.user.avatar).decode('utf-8') if ad_request.campaign.campaigner.user.avatar else ad_request.campaign.campaigner.user.avatar)(ad_request) if ad_request else None,
            'sponsor_id': ad_request.campaign.campaigner.id if ad_request else None,
            'requestExist': True if ad_request else False,
            'message': ad_request.message if ad_request else None,
            'requirements': ad_request.requirements if ad_request else None,
            'payment': ad_request.payment if ad_request else None,
            'status': ad_request.status.name if ad_request else None,  # Assuming you want to show the status name
            'time': ad_request.time if ad_request else None
        }
    ]

    return jsonify({'db_data': requests_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200








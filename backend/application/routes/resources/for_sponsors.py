from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_accepted, current_user

from application.setup.models import db, AdRequests, Campaigns, Users, Influencers
from application.setup.errors import ResourceNotFoundError
from application.setup.functions import safe_get
from sqlalchemy import asc, desc, and_, case, func
from datetime import datetime
import base64 , calendar
import time

sponsor_resources = Blueprint('Sponsor-resources', __name__ )


@sponsor_resources.get('/sponsors-dashboard-details')
@auth_required('token')
@roles_accepted('Sponsor')
def sponsors_dashboard_details():
    """
    1. total campaigns : count 
    2. Total pending requests : count
    3. investment in current month : budget's sum 
    4. investment in current year : budget's sum 
    """
    ####################################################################################################
    total_campaigns = db.session.query(
        func.count(Campaigns.id).label('campaign_count')
   ).filter(
        Campaigns.creater_id_which_is_a_sponsor == current_user.sponsor_details.id
    ).scalar()
    ####################################################################################################





    ####################################################################################################
    total_pending_requests = db.session.query(
        func.count(AdRequests.id).label('pending_request_count')
    ).join(Campaigns, AdRequests.campaign_id == Campaigns.id)\
     .filter(
        AdRequests.status == 'PENDING',
        Campaigns.creater_id_which_is_a_sponsor == current_user.sponsor_details.id
    ).scalar()
    ####################################################################################################




    ####################################################################################################
    current_year = datetime.now().year
    current_month = datetime.now().month
    # Get the first and last days of the current month
    first_day_of_month = datetime(current_year, current_month, 1)
    last_day_of_month = datetime(current_year, current_month, calendar.monthrange(current_year, current_month)[1])
    # Query campaigns within the current month
    current_month_result = db.session.query(
        func.sum(Campaigns.budget).label('total_budget'),
        func.count(Campaigns.id).label('campaign_count')
    ).filter(
        Campaigns.time.between(first_day_of_month, last_day_of_month),
        Campaigns.creater_id_which_is_a_sponsor == current_user.sponsor_details.id 
    ).one_or_none()
    ####################################################################################################



    ####################################################################################################
    current_year = datetime.now().year
    # Get the first day and last day of the current year
    first_day_of_year = datetime(current_year, 1, 1)
    last_day_of_year = datetime(current_year, 12, 31)
    # Query to get both the sum of budgets and the count of campaigns
    current_year_result = db.session.query(
        func.sum(Campaigns.budget).label('total_budget'),
        func.count(Campaigns.id).label('campaign_count'),
    ).filter(
        Campaigns.time.between(first_day_of_year, last_day_of_year),
        Campaigns.creater_id_which_is_a_sponsor == current_user.sponsor_details.id  
    ).one_or_none()
    ####################################################################################################




    ####################################################################################################
    # charts
    ####################################################################################################

    db_data = {
        'stats': {
            'total_campaigns': total_campaigns,
            'total_pending_requests': total_pending_requests,
            'current_month': {
                'investment':current_month_result.total_budget or 0,
                'campaign_count' : current_month_result.campaign_count
            },
            'current_year': {
                'investment': current_year_result.total_budget or 0,
                'campaign_count' : current_year_result.campaign_count
            }
        },
        'charts' :{

        }
    }

    return jsonify({'db_data': db_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@sponsor_resources.get('/search-by-sponsors')
@auth_required('token')
@roles_accepted('Sponsor')
def search_by_sponsors():
    # code for search for influencers
    # should be able to search for relevant influencers based on their niche, reach, category etc.
    # and return list of influencers with their details
    query = request.args.get('query', '')
    queryList = query.lower().split(' ')

    base_query = db.session.query(
        Users.id.label('influencer_s_user_id'),
        Users.name.label('name'),
        Users.username.label('username'),
        Users.avatar.label("avatar"),
        Influencers.id.label("influencer_id"),
        Influencers.category.label("category"),
        Influencers.niche.label("niche"),
        Influencers.reach.label("reach"),
        Influencers.description.label("description"),
        Influencers.link.label("link"),
    ).join(Users, Influencers.user_id == Users.id)

    search_filters = []
    if 'niche' in queryList:
        parameter = safe_get(queryList,queryList.index('niche')+1)
        search_filters.append(Influencers.niche.ilike(f"%{parameter}%"))
    if 'category' in queryList:
        parameter = safe_get(queryList,queryList.index('category')+1)
        search_filters.append(Influencers.category.ilike(f"%{parameter}%"))
    if 'reach' in queryList:
        parameter = safe_get(queryList,queryList.index('reach')+1)
        search_filters.append(Influencers.reach.ilike(f"%{parameter}%"))
    if 'username' in queryList:
        parameter = safe_get(queryList,queryList.index('username')+1)
        search_filters.append(Users.username.ilike(f"%{parameter}%"))
    if 'name' in queryList:
        parameter = safe_get(queryList,queryList.index('name')+1)
        search_filters.append(Users.name.ilike(f"%{parameter}%"))

    if search_filters:
        base_query = base_query.filter(db.or_(*search_filters))
    else:
        base_query = base_query.filter(Influencers.description.ilike(f"%{query}%"))

    all_influencers = base_query.all()

    influencers_data = [
        {
            'influencer_id': influencer.influencer_id,
            'category': influencer.category,
            'niche': influencer.niche,
            'reach': influencer.reach,
            'description': influencer.description,
            'link': influencer.link,
            'influencer_s_user_id': influencer.influencer_s_user_id,
            'username': influencer.username,
            'name': influencer.name,
            'avatar': base64.b64encode(influencer.avatar).decode('utf-8') if influencer.avatar else influencer.avatar
        } for influencer in all_influencers 
    ]

    return jsonify({'db_data': influencers_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@sponsor_resources.get('/all-campaigns-of-a-sponsor')
@auth_required('token')
@roles_accepted('Sponsor')
def all_campaigns_of_a_sponsor():
    # Extract request parameters
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', '')
    search_on = request.args.get('searchOn', '')

    # print(limit, offset, sort_by, order, search, search_on)
    sponsor_id = current_user.sponsor_details.id      

    # Initial query to get the total number of records for the sponsor without filters
    base_query = Campaigns.query.filter_by(creater_id_which_is_a_sponsor=sponsor_id)
    records_total = base_query.count()

    # Build the query with search filter if provided
    query = base_query
    if search and search_on:
        columns_to_search = search_on.split(',')

        # print(columns_to_search)
        # Create search filters for each column
        search_filters = []
        for col in columns_to_search:
            if hasattr(Campaigns, col):  # Check if the column exists in the Campaigns model
                filter_condition = getattr(Campaigns, col).ilike(f"%{search}%")
                search_filters.append(filter_condition)
        
        # Apply OR filter for the search conditions
        if search_filters:  # Only apply if there are any filters
            query = query.filter(db.or_(*search_filters))

    # Count records after filtering
    records_filtered = query.count()

    # Apply sorting and pagination
    sort_column = getattr(Campaigns, sort_by, Campaigns.id)
    query = query.order_by(asc(sort_column) if order == 'asc' else desc(sort_column))
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
            'time': campaign.time
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



@sponsor_resources.get('/all-requests-of-a-sponsor')
@auth_required('token')
@roles_accepted('Sponsor')
def all_requests_of_a_sponsor():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search', '')
    search_on = request.args.get('searchOn', '')
    

    # Get the current sponsor's ID
    sponsor_id = current_user.sponsor_details.id

    # Query to retrieve ad requests with related campaign and influencer details
    base_query = db.session.query(
        AdRequests.id,
        AdRequests.message,
        AdRequests.requirements,
        AdRequests.payment,
        AdRequests.status,
        AdRequests.time,
        Campaigns.id.label('campaign_id'),
        Campaigns.name.label('campaign_name'),
        Users.id.label('influencer_s_user_id'),
        Users.username.label('influencer_username')
    ).join(Campaigns, AdRequests.campaign_id == Campaigns.id) \
    .join(Influencers, AdRequests.influencer_id == Influencers.id) \
    .join(Users, Influencers.user_id == Users.id) \
    .filter(Campaigns.creater_id_which_is_a_sponsor == sponsor_id)

    # Add search functionality if provided
    if search and search_on:
        columns_to_search = search_on.split(',')
        search_filters = []
        for col in columns_to_search:
            if col == 'campaign_name':
                search_filters.append(Campaigns.name.ilike(f"%{search}%"))
            elif col == 'influencer_username':
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
    elif sort_by == 'influencer_username':
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
            'influencer_s_user_id': ad_request.influencer_s_user_id,
            'influencer_username': ad_request.influencer_username,
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



@sponsor_resources.get('/all-influencers-profiles')
@auth_required('token')
@roles_accepted('Sponsor','Admin')
def all_influencers():
    influencers = Influencers.query.all()

    influencers_data = [
        {
            'influencer_id':influencer.id,
            'category':influencer.category,
            'niche':influencer.niche,
            'reach': influencer.reach,
            'description':influencer.description,
            'link':influencer.link,
            'influencer_s_user_id':influencer.user.id,
            'username':influencer.user.username,
            'name':influencer.user.name,
            'avatar':base64.b64encode(influencer.user.avatar).decode('utf-8') if influencer.user.avatar else influencer.user.avatar,
            'isActive':influencer.user.is_active
        }
        for influencer in influencers
    ]

    return jsonify({'db_data': influencers_data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}), 200



@sponsor_resources.get('/all-influencers-for-each-campaign-page/<int:campaign_id>')
@auth_required('token')
@roles_accepted('Sponsor')
def all_influencers_for_each_campaign_page(campaign_id):
    """
    Query to get all influencers for a specific campaign, including those with
    and without ad requests. Filters based on campaign category
    sorted by request exist or not

    columns:
        influencer_s_user_id
        influencer_username
        influencer_category
        ---if request exists---
        adRequest_id
        time
        message
        requirements
        payment
        status


    SELECT 
        influencers.id AS influencer_id,
        influencers.category AS influencer_category,
        users.username AS influencer_username,
        CASE 
            WHEN ad_requests.id IS NOT NULL THEN TRUE
            ELSE FALSE
        END AS requestExist,
        ad_requests.id AS adRequest_id,
        ad_requests.time AS time,
        ad_requests.message AS message,
        ad_requests.requirements AS requirements,
        ad_requests.payment AS payment,
        ad_requests.status AS status
    FROM 
        influencers
    LEFT JOIN 
        ad_requests ON influencers.id = ad_requests.influencer_id 
        AND ad_requests.campaign_id = 2
    JOIN 
        users ON users.id = influencers.user_id
    ORDER BY 
        requestExist DESC,  -- First, prioritize influencers with requests (requestExist = TRUE)
        CASE 
            WHEN influencer_category LIKE '%sd%' THEN 0  -- Prioritize influencers with requestExist TRUE and matching category
            ELSE 1  -- Then, influencers with no request but matching category
        END,
        influencer_category asc; 

        left table is determine by the class in query if multiple are there then depends on first join condition's second argument anyone would be taken. 
    """
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
     .outerjoin(AdRequests, 
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


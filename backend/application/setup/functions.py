from functools import wraps
from flask_security import current_user
from datetime import datetime
from .models import  Users , AdRequests , Sponsors , Influencers , Campaigns, Chats
from .errors import UserNotFoundError, UserAlreadyExists, ResourceNotFoundError, ResourceAlreadyExists, BadRequest, OwnershipRequired, InternalServerError

def ownership_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # print(kwargs)

        id_name = list(kwargs.keys())[0]
        id = kwargs[list(kwargs.keys())[0]]

        if not id:
            raise InternalServerError(error_message="ID is required")
        
        elif id_name == "user_id":
            obj = Users.query.get(id)
            if not obj:
                raise UserNotFoundError()
            elif obj.id != current_user.id:
                raise OwnershipRequired()

                    
        elif id_name == "sponsor_id":
            obj = Sponsors.query.get(id)
            if not obj:
                raise ResourceNotFoundError(error_message='Sponsor not found')
            elif obj.user_id != current_user.id:
                raise OwnershipRequired()   
            
        elif id_name == "influencer_id":
            obj = Influencers.query.get(id)
            if not obj:
                raise ResourceNotFoundError(error_message='Influencer not found')
            elif obj.user_id != current_user.id:
                raise OwnershipRequired()   

        elif id_name == "campaign_id":
            obj = Campaigns.query.get(id)
            if not obj:
                raise ResourceNotFoundError(error_message='Influencer not found')
            elif obj.campaigner.user_id != current_user.id:
                raise OwnershipRequired()   

        elif id_name == "chat_id":
            obj = Chats.query.get(id)
            if not obj:
                raise ResourceNotFoundError(error_message='Chat not found')
            elif obj.commenter_id != current_user.id:
                raise OwnershipRequired()   
            
        elif id_name == "adRequest_id":
            obj = AdRequests.query.get(id)
            if not obj:
                raise ResourceNotFoundError(error_message='AdRequest not found')
            elif "Sponsor" in current_user.roles and obj.campaign.campaigner.user_id != current_user.id:
                raise OwnershipRequired(error_message='You are a sponsor and trying to access others adRequests.')   
            elif "Influencer" in current_user.roles and obj.influencer.user_id != current_user.id:
                raise OwnershipRequired(error_message='You are a influencer and trying to access others adRequests.')   

        return func(*args, **kwargs)
    
    return decorated_function

import re

def email_format(email):
    pattern = r'^[a-zA-Z0-9.]+@gmail\.com$'
    return re.match(pattern, email)


def date_type(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise BadRequest(error_message='Invalid date format. Use YYYY-MM-DD')

def time_type(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        raise BadRequest(error_message='Invalid time format. Use HH:MM')
    

def safe_get(lst, index, default=None):
    return lst[index] if index < len(lst) else default
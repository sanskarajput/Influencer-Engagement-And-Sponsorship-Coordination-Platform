from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from .models import db, Influencers, Users,Sponsors




def create_data(user_datastore : SQLAlchemyUserDatastore):
    user_datastore.find_or_create_role(name= 'Admin', description= "An administrator can monitor all the users/campaigns, see all the statistics nad have ability to flag inappropriate campaigns/users")
    user_datastore.find_or_create_role(name= 'Sponsor', description= "Company/individual who wants to advertise their product/service Sponsors will create campaigns, search for influencers and send ad requests for a particular campaign. Sponsors can create multiple campaigns and track each individual campaign. They can accept ad requests by influencers for public campaigns.")
    user_datastore.find_or_create_role(name= 'Influencer', description= "An influencer will receive ad requests, accept or reject ad requests, negotiate terms and resend modified ad requests back to sponsors. They can search for ongoing campaigns (which are public), according to category, budget etc. and accept the request. An influencer can update their profile page, which is publicly visible.")

    if not user_datastore.find_user(email = "admin.app@example.com"):
        user_datastore.create_user(email = "admin.app@example.com", password = hash_password('pass'), roles=['Admin'], name="Sanskar", username= "San_skar__")

    db.session.commit()


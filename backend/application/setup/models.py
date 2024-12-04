from .database import db
from flask_security import UserMixin , RoleMixin , current_user
from sqlalchemy import func
from sqlalchemy import Enum as SQLAEnum
from enum import Enum


UserRole = db.Table('user_role',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), primary_key = True, unique = True),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'), primary_key = True)
    )


class Users(db.Model, UserMixin):
    __tablename__  = "users"
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(55), nullable = False , unique = True)
    password = db.Column(db.String(500), nullable = False , unique = True)
    active = db.Column(db.Boolean(), default = True)
    fs_uniquifier = db.Column(db.String(500), nullable = False)
    
    username = db.Column(db.String(50),  unique = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    avatar = db.Column(db.LargeBinary())
    time = db.Column(db.DateTime, default=func.now())

    roles = db.relationship("Roles", secondary = UserRole, backref = "users")

    sponsor_details = db.relationship("Sponsors", uselist=False , backref='user',cascade="all,delete")
    influencer_details = db.relationship("Influencers", uselist=False , backref='user',cascade="all,delete")

    def __repr__(self):
        return f'<User {self.id}>'



class Roles(db.Model, RoleMixin):
    __tablename__  = "roles"
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(50), nullable = False , unique = True)
    description = db.Column(db.String())

    def __repr__(self):
        return f'<Role {self.id}>'


class Sponsors(db.Model):
    __tablename__ = "sponsors"
    id = db.Column(db.Integer(),primary_key = True)
    typee = db.Column(db.String(50), nullable = False,default="Individual") # company/individual
    industry = db.Column(db.String(50), nullable = True)
    budget = db.Column(db.Float(), nullable = True)
    description = db.Column(db.String(), nullable = True)
    approved = db.Column(db.String(50), nullable = False, default="PENDING") # TRUE, FALSE
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False, unique = True)

    campaigns = db.relationship("Campaigns", backref='campaigner', cascade="all,delete", lazy=True)

    def __repr__(self):
        return f'<Sponsor {self.id}>'
    

class Influencers(db.Model):
    __tablename__ = "influencers"
    id = db.Column(db.Integer(),primary_key = True)
    category = db.Column(db.String(50), nullable = True , default='Lifestyle')
    niche = db.Column(db.String(50), nullable = True)
    reach  = db.Column(db.Integer(), nullable = True)
    description = db.Column(db.String(), nullable = True)
    link = db.Column(db.String(), nullable = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False, unique = True)

    all_adRequests = db.relationship("AdRequests", backref='influencer', cascade="all,delete", lazy=True)

    def __repr__(self):
        return f'<Influencer {self.id}>'
    

class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer(),primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(50), nullable = False)
    category = db.Column(db.String(150), nullable = False)
    start_date = db.Column(db.DateTime, nullable = False)   
    end_date = db.Column(db.DateTime, nullable = False)
    budget = db.Column(db.Float(), nullable = False)
    visibility = db.Column(db.String(), nullable = False, default = 'PUBLIC')
    goals = db.Column(db.String(1000), nullable = False)
    time = db.Column(db.DateTime, default=func.now())
    flagged = db.Column(db.Boolean(), default=False)
    creater_id_which_is_a_sponsor = db.Column(db.Integer(), db.ForeignKey('sponsors.id'), nullable = False)

    __table_args__ = (db.UniqueConstraint('creater_id_which_is_a_sponsor', 'name', name = 'Unique_creater_id_which_is_a_sponsor_name'),)

    all_adRequests = db.relationship("AdRequests", backref='campaign', cascade="all,delete", lazy=True)

    def __repr__(self):
        return f'<Campaign {self.id}>'
    

class RequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    COMPLETED = "completed"
    REJECTED = "rejected"

    @classmethod
    @property
    def keys(cls):
        return [key.name for key in cls]

    @classmethod
    @property
    def values(cls):
        return [key.value for key in cls]


class AdRequests(db.Model):
    __tablename__ = "ad_requests"
    id = db.Column(db.Integer(),primary_key = True)
    campaign_id = db.Column(db.Integer(), db.ForeignKey('campaigns.id'), nullable = False)
    influencer_id = db.Column(db.Integer(), db.ForeignKey('influencers.id'), nullable = False)
    message = db.Column(db.String(1000), nullable = False, default="dumy message")
    requirements = db.Column(db.String(1000), nullable = False, default="dumy requirements")
    payment = db.Column(db.Float(), nullable = False, default = 0.0)
    status = db.Column(SQLAEnum(RequestStatus), default=RequestStatus.PENDING)
    time = db.Column(db.DateTime, default=func.now())

    __table_args__ = (db.UniqueConstraint('campaign_id', 'influencer_id', name = 'Unique_influencer_campaign'),)

    chats = db.relationship("Chats", backref='adRequest', cascade="all,delete", lazy=True)
 
    def __repr__(self):
        return f'<AdRequest {self.id}>'


class Chats(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer(),primary_key = True)
    commenter = db.Column(db.String(), nullable = False)
    comment = db.Column(db.String(2000), nullable = False)
    time = db.Column(db.DateTime, default=func.now())
    adRequest_id = db.Column(db.Integer(), db.ForeignKey('ad_requests.id'), nullable = False)
    commenter_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)

    def __init__(self,comment,adRequest_id):
        self.comment = comment
        self.adRequest_id = adRequest_id
        self.commenter_id = current_user.id
        roles = [role.name for role in current_user.roles]
        if 'Influencer' in roles:
            self.commenter = 'Influencer'
        elif 'Sponsor' in roles:
            self.commenter = 'Sponsor'
        else:
            self.commenter = 'Admin'

    def __repr__(self):
        return f'<Chat {self.id}>'

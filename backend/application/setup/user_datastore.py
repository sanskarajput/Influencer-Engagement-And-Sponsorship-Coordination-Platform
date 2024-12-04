from .models import db, Users, Roles
from flask_security import SQLAlchemyUserDatastore

user_datastore = SQLAlchemyUserDatastore(db, Users, Roles) 

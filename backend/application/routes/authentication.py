from flask import Blueprint, jsonify
from flask_security.utils import hash_password, verify_password

from application.setup.user_datastore import user_datastore
from application.setup.models import Influencers, Sponsors, db

from application.setup.functions import email_format
from application.setup.errors import UserNotFoundError, UserAlreadyExists, ResourceNotFoundError, ResourceAlreadyExists, BadRequest, OwnershipRequired, InternalServerError
from flask_restful import Api, reqparse, Resource


auth = Blueprint('authentication', __name__ )
api = Api(auth)


parser_signup = reqparse.RequestParser()
parser_signup.add_argument("email" , required = True , type = str, help="email cannot be blank and must be a string !")
parser_signup.add_argument("username" , required = True , type = str, help="username cannot be blank and must be a string !")
parser_signup.add_argument("name" , required = True , type = str, help="name cannot be blank and must be a string !")
parser_signup.add_argument("role" , required = True , type = str, help="role cannot be blank and must be a string !")
# parser_signup.add_argument("avatar" , required = False, default = None , type = str, help="avatar must be file !")
parser_signup.add_argument("password" , required = True , type = str, help="password cannot be blank and must be a string !")


class Signup(Resource):
    def post(self):
        args = parser_signup.parse_args()
        email = args.get('email')
        username = args.get('username')
        name = args.get('name')  
        password = args.get('password')
        # avatar = args.get('avatar')  # have to do some work  # bad me update kar sakte
        role = args.get('role')

        if not email or not username or not password or not name or not role:
            raise BadRequest(error_message='Missing required field')
        
        try:
            role = role.capitalize()
        except ValueError:
            raise BadRequest(error_message='Invalid role')
        
        if role not in ['Sponsor','Influencer']:
            raise BadRequest(error_message='Invalid role')

        # here check provided email address is valid on google account
        if user_datastore.find_user(email = email):
            raise UserAlreadyExists(error_message='email address already exists')

        if user_datastore.find_user(username = username):
            raise UserAlreadyExists(error_message='username already exists')
        
        try:
            user_datastore.create_user(email = email, password = hash_password(password), username = username, name = name , roles = [ role ])
            db.session.commit()
            if role == 'Influencer':
                new_influencer = Influencers()
                new_influencer.user_id = user_datastore.find_user(email = email).id    # try to improve by `user_datastore.find_user(email = email)`
                db.session.add(new_influencer)
            elif role == 'Sponsor':
                new_sponsor = Sponsors()
                new_sponsor.user_id = user_datastore.find_user(email = email).id
                db.session.add(new_sponsor)
            db.session.commit()
            return {'db_data': {},
                    'code'   : 'SUCCESS',
                    'message': 'Registration successful'}, 201
        except Exception as e:
            db.session.rollback()
            raise InternalServerError(error_message=str(e))





parser_login = reqparse.RequestParser()
parser_login.add_argument("emailORusername" , type = str, required = True, help="emailORusername cannot be blank and must be a string !")
parser_login.add_argument("password"        , type = str, required = True, help="password cannot be blank and must be a string !")

class Login(Resource):
    def post(self):
        args = parser_login.parse_args()
        emailORusername = args.get('emailORusername')
        password = args.get('password')

        if not emailORusername or not password:
            raise BadRequest(error_message='Missing required field')
        
        # if email_format(emailORusername):
        if True:
            user = user_datastore.find_user(email = emailORusername)
        else:
            user = user_datastore.find_user(username = emailORusername)

        if not user:
           raise UserNotFoundError(error_message='User not found')
        
        if not verify_password(password, user.password):
            raise BadRequest(error_message='incorrect password')

        try:
            data = {'auth_token':user.get_auth_token(), 
                    'id':user.id,
                    'email':user.email, 
                    'username':user.username,
                    'name':user.name,
                    'role':[role.name for role in user.roles][0],
                    'role_id': (lambda user: user.influencer_details.id if user.influencer_details else (user.sponsor_details.id if user.sponsor_details else 0))(user),
                    'time':str(user.time),
                    'is_active':user.is_active,
                    'is_anonymous':user.is_anonymous,
                    'is_authenticated':user.is_authenticated
                    } 
            
            # Flask-Restful automatically serializes dictionaries into JSON and handles the Response generation internally. By returning a dictionary directly, you avoid the error caused by trying to serialize a Response object.
            return {'db_data':  data,
                    'code'   : 'SUCCESS',
                    'message': 'Operations completed successfully'}, 200
        except Exception as e:
            raise InternalServerError(error_message='While parseing json some error occurred')


api.add_resource(Signup , "/my-signup")   
api.add_resource(Login , "/my-login")   

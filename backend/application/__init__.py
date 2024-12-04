# __init__.py


def set_configuration(app):
    app.config['SECRET_KEY'] = "should-not-be-exposed"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
    app.config['SECURITY_PASSWORD_SALT'] = 'salty-password'
    app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Auth-Token"
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config['CACHE_KEY_PREFIX'] = "mycahce"
    app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/1"
    # app.config['SECURITY_TOKEN_MAX_AGE'] = 15

    return app


def binding_db_with_app(app):
    from application.setup.models import db
    db.init_app(app)    
    return app, db


def initialize_user_datastore():
    import application.setup.user_datastore as user_data
    return user_data.user_datastore 
    

def setup_flask_security(app,user_datastore):
    from flask_security import Security
    security = Security(app, user_datastore) 
    return app


def create_db(app,db):
    with app.app_context():
        db.create_all()
    return db



def creating_necessary_data(app,user_datastore):
    with app.app_context():
        from application.setup.data import create_data
        create_data(user_datastore)


def registering_blueprints(app):
    from application.routes.authentication import auth
    app.register_blueprint(auth)    
    
    from application.routes.sponsors import spon
    app.register_blueprint(spon)                    

    from application.routes.influencers import influ
    app.register_blueprint(influ)          

    from application.routes.admin import admin
    app.register_blueprint(admin)                        
    
    from application.routes.campaigns import campaign
    app.register_blueprint(campaign, url_prefix='/campaign')

    from application.routes.ad_requests import adRequest
    app.register_blueprint(adRequest, url_prefix='/request')

    from application.routes.chats import chat
    app.register_blueprint(chat, url_prefix='/requests/<int:reqId>/chat')

    from application.routes.errors import err
    app.register_blueprint(err)


    from application.routes.resources.for_sponsors import sponsor_resources
    app.register_blueprint(sponsor_resources)

    from application.routes.resources.for_influencers import influencer_resources
    app.register_blueprint(influencer_resources)

    from application.routes.resources.for_admin import admin_resources
    app.register_blueprint(admin_resources)


    return app






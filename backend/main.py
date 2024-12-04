import application
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from application.setup.celery.worker import celery_init_app
from application.setup.celery.task import sending_mail_to_influencers_if_they_have_pending_request, monthly_report_for_sponsors_of_their_campaign
from celery.schedules import crontab


app = Flask(__name__)

CORS(app)

def create_app(app):
    app = application.set_configuration(app)
    app , db = application.binding_db_with_app(app)
    user_datastore = application.initialize_user_datastore()
    app = application.setup_flask_security(app, user_datastore)
    db = application.create_db(app,db)
    application.creating_necessary_data(app,user_datastore)
    application.registering_blueprints(app)
    celery_app = celery_init_app(app)   
    return app,celery_app

app, celery_app = create_app(app)
cache = Cache(app)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=11, minute=0),
        sending_mail_to_influencers_if_they_have_pending_request.s(),
        name='daily reminders for influences',
    )
    sender.add_periodic_task(
        crontab(hour=12, minute=0, day_of_month='last'),
        monthly_report_for_sponsors_of_their_campaign.s(),
        name='last_day_of_month',
    )


if __name__ == "__main__" :
    app.run(host='0.0.0.0',port=5000,debug = True)

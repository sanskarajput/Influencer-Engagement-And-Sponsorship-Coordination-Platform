from celery import Celery, Task

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    
    # Provide configuration here directly
    celery_app.conf.update(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0', 
        broker_connection_retry_on_startup = True,
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],    
        timezone='Asia/Kolkata',
        enable_utc=False,
    )
    
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

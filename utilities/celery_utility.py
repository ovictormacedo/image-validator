from celery import Celery
from settings import CELERY_URL

def make_celery(app):
    # Celery settings
    app.config['CELERY_BROKER_URL'] = CELERY_URL
    app.config['CELERY_RESULT_BACKEND'] = CELERY_URL

    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
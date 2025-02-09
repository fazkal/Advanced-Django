import os
from celery import Celery
from accounts.tasks import sendEmail

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'core.settings')

app=Celery('core')

app.config_from_object('django.conf:settings' , namespace='CELERY')

app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0 , sendEmail.s() , name="send email every 10 seconds")
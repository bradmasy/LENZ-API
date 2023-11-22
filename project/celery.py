from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import dotenv

dotenv.load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete-expired-photos": {
        "task": "photo.tasks.delete_expired_photos",
        "schedule": crontab(minute=0, hour=0),  # Run daily at midnight
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# from celery import Celery

# app = Celery('project',
#              broker='amqp://',
#              backend='rpc://')

# # Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )

# if __name__ == '__main__':
#     app.start()

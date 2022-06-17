import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery beat tasks

# Настройка расписания celery beat
# Добавляем функцию обновления базы данных
app.conf.beat_schedule = {
    'update-orders-info-every-1-minute': {
        'task': 'main.tasks.update_orders_info_task',
        'schedule': crontab(minute='*/1'),
    },
}


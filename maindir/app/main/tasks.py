from app.celery import app
from script import update_orders_info


@app.task
def update_orders_info_task():
    """Задача, вызывающаяся celery beat каждую минуту"""
    update_orders_info()

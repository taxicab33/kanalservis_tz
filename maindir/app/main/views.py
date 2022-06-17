import json
from django.http import HttpResponse

# Create your views here.
from django.views.generic import ListView

from main.models import Order
from main.services import get_orders_data


class OrderListView(ListView):
    """Представление для получения записей таблицы заказов"""
    model = Order
    template_name = 'main/main.html'
    context_object_name = 'orders'


def get_data(request):
    """Функция для получения графиком данных о заказах"""
    return HttpResponse(json.dumps(get_orders_data()), content_type="application/json")

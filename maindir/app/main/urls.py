from django.urls import path, include
from main.views import get_data, OrderListView

urlpatterns = [
    path('', OrderListView.as_view()),
    path('get_data', get_data)
]
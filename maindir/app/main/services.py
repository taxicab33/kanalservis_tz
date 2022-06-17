from main.models import Order


def get_orders_data():
    """Получаем данные для построения графика"""
    orders = Order.objects.all()
    data = []
    for item in orders:
        order_dict = dict()
        daily_sales = 0
        if str(item.delivery_date) not in order_dict.values():
            for item2 in orders:
                if item.delivery_date == item2.delivery_date:
                    daily_sales += item2.rub_price
            order_dict = {"date": str(item.delivery_date),
                          "units": daily_sales}
        data.append(order_dict)
    return data

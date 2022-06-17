from django import template

register = template.Library()


@register.filter(name='sum_rub_price')
def sum_rub_price(self, column_name):
    """Считаем общую сумму заказов в рублях внутри шаблона"""
    total = 0
    for item in self:
        total += getattr(item, column_name)
    return round(total, 2)
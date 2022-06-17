from django.db import models


class Order(models.Model):
    """Модель заказа"""
    article = models.CharField(max_length=7, verbose_name="Номер заказа", unique=True, db_index=True, primary_key=True)
    price = models.FloatField(verbose_name="Стоимость, $")
    rub_price = models.FloatField(verbose_name="Стоимость, RUB")
    delivery_date = models.DateField(verbose_name="Срок доставки")

    def __eq__(self, other):
        """Переопределение функции равно __eq__ данного класса. Здесь сравниваются все поля, кроме первичного ключа"""
        equal = True
        if self.price != other.price:
            equal = False
        if self.rub_price != other.rub_price:
            equal = False
        if self.delivery_date != other.delivery_date:
            equal = False
        return equal

    class Meta:
        """Класс, определяющий метаданные, в данном случае - сортировку выборки"""
        ordering = ['delivery_date']

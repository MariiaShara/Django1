from django.db import models
from django.contrib.auth import get_user_model

from mainapp.models import Clothing

class ShoppingCartItem(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='shopping_bag',
        verbose_name='user')
    product = models.ForeignKey(
        Clothing,
        on_delete=models.CASCADE,
        verbose_name='product name')
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='product quantity')
    add_datetime = models.DateTimeField(
        verbose_name='time',
        auto_now_add=True)

    def product_ttl_price(self):
        return (self.product.price * self.quantity)


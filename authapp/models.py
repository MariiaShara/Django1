from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.urls import reverse
from django.conf import settings
from hautelookstore.settings import USER_EXPIRES_TIMEDELTA


def get_activation_key_expires():
    return now() + USER_EXPIRES_TIMEDELTA


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='age')
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(
        default=get_activation_key_expires
    )

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def send_verify_mail(self):
        verify_link = reverse(
            'auth:user_verify',
            kwargs={
                'email': self.email,
                'activation_key': self.activation_key
            }
        )

        title = f'{self.username} activation'

        message = f'{self.username} to confirm your registration at ' \
                  f'{settings.DOMAIN_NAME} please click on the link below: \n' \
                  f'{settings.DOMAIN_NAME}{verify_link}'

        return self.email_user(
            title, message, settings.EMAIL_HOST_USER, fail_silently=False
        )

    def bag_ttl_price(self):
        return sum(item.product.price * item.quantity for item in self.shopping_bag.all())

    def bag_ttl_quantity(self):
        return sum(item.quantity for item in self.shopping_bag.all())

    class Meta:
        ordering = ['-is_active', '-is_superuser', '-is_staff', 'username']

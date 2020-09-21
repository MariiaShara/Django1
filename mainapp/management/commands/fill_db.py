import os
import json

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ClothingCategory, Clothing
from django.conf import settings

def load_from_json(file_name):
    with open(
            os.path.join(settings.JSON_PATH, f'{file_name}.json'),
            encoding='utf-8'
    ) as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill DB with new data'

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ClothingCategory.objects.all().delete()
        [ClothingCategory.objects.create(**category) for category in categories]

        clothings = load_from_json('clothings')

        Clothing.objects.all().delete()
        for clothing in clothings:
            category_name = clothing['category']
            # Получаем категорию по имени
            _category = ClothingCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            clothing['category'] = _category
            new_clothing = Clothing(**clothing)
            new_clothing.save()

        # Создаем суперпользователя при помощи менеджера модели
        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser(username='django', email='django@geekshop.local', password='geekbrains', age='33')

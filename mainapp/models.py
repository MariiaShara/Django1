from django.db import models


class ClothingCategory(models.Model):
    name = models.CharField(verbose_name='category name', max_length=128)
    description = models.TextField(verbose_name='category description', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Clothing(models.Model):
    category = models.ForeignKey(ClothingCategory,
                                 on_delete=models.CASCADE,
                                 verbose_name='clothing category')
    name = models.CharField(verbose_name='clothing name', max_length=128)
    image = models.ImageField(upload_to='clothings_images', blank=True)
    short_descript = models.CharField(verbose_name='clothing short description',
                                      max_length=64,
                                      blank=True)
    description = models.TextField(verbose_name='clothing description', blank=True)
    designer_info = models.TextField(verbose_name='about designer', blank=True)
    price = models.DecimalField('clothing price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField('quantity at warehouse', default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'clothing'
        verbose_name_plural = 'clothings'

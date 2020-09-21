from mainapp.models import ClothingCategory


def catalogue_menu(request):
    return {
        'catalogue_menu': ClothingCategory.objects.filter(is_active=True),
    }
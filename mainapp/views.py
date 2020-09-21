import random

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mainapp.models import ClothingCategory, Clothing


def exclusive_products():
    products_id = Clothing.objects.filter(price__lt=200).values_list('id', flat=True)
    exclusive_products_id = random.sample(list(products_id), 4)
    return Clothing.objects.filter(pk__in=exclusive_products_id)


def trending_products():
    products_id = list(Clothing.objects.values_list('id', flat=True))
    trending_products_id = random.sample(products_id, 8)
    return Clothing.objects.filter(pk__in=trending_products_id)


def featured_products():
    products_id = Clothing.objects.filter(price__gt=200).values_list('id', flat=True)
    featured_products_id = random.sample(list(products_id), 4)
    return Clothing.objects.filter(pk__in=featured_products_id)


def index(request):
    _exclusive_products = exclusive_products()
    _trending_products = trending_products()
    _featured_products = featured_products()
    context = {
        'page_title': 'home',
        'excl_products': _exclusive_products,
        'trending_products': _trending_products,
        'featured_products': _featured_products,
    }
    return render(request, 'mainapp/index.html', context)


def get_hot_deal():
    products_id = Clothing.objects.values_list('id', flat=True)
    hot_product_id = random.choice(products_id)
    return Clothing.objects.get(pk=hot_product_id)


def related_products(product):
    return Clothing.objects.filter(category=product.category).exclude(id=product.id)[:4]


def products(request):
    hot_product = get_hot_deal()
    _related_products = related_products(hot_product)

    context = {
        'page_title': 'products',
        'hot_product': hot_product,
        'related_products': _related_products,
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    context = {
        'page_title': 'product',
        'product': get_object_or_404(Clothing, pk=pk),
    }
    return render(request, 'mainapp/product.html', context)


def catalogue(request, pk, page=1):
    if int(pk) == 0:
        category = {'pk': 0, 'name': 'all'}
        products = Clothing.objects.all()
    else:
        category = get_object_or_404(ClothingCategory, pk=pk)
        products = Clothing.objects.filter(category=category)

    products_paginator = Paginator(products, 2)
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context = {
        'page_title': 'catalogue',
        'category': category,
        'products': products,
    }
    return render(request, 'mainapp/catalogue.html', context)


def contacts(request):
    locations = [
        {
            'state': 'Dictrict of Columbia',
            'phone': '+1-202-400-8960',
            'email': 'info@hautelook.com',
            'address': '3589 Massachusets Ave NW, Washington DC, 2007'
        },
        {
            'state': 'Washington',
            'phone': '+1-206-456-8967',
            'email': 'customerservice@hautelook.com',
            'address': '3475 1sr Ave NW, Seattle WA, 21304'
        },
        {
            'state': 'California',
            'phone': '+1-203-456-1111',
            'email': 'returns@hautelook.com',
            'address': '2300 Florida Ave SW, Los Angeles CA, 34029'
        }
    ]

    context = {
        'page_title': 'contacts',
        'locations': locations,
    }
    return render(request, 'mainapp/contacts.html', context)

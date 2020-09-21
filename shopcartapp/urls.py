"""hautelookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

import shopcartapp.views as shopcart

app_name = 'shopcart'

urlpatterns = [
    path('', shopcart.index, name='index'),
    path('add/product/<int:pk>/', shopcart.add, name='add'),
    path('delete/cart/item/<int:pk>/', shopcart.delete, name='delete'),
    path('change/<int:pk>/quantity/<int:quantity>/', shopcart.change, name='change'),
]

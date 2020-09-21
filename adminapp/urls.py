from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.UsersList.as_view(), name='index'),
    path('user/add/', adminapp.user_add, name='user_add'),
    path('user/<int:pk>/edit/', adminapp.user_edit, name='user_edit'),
    path('user/<int:pk>/delete/', adminapp.user_delete, name='user_delete'),

    path('categories/read/', adminapp.CategoriesRead.as_view(), name='categories_read'),
    path('category/add/', adminapp.CategoryAdd.as_view(), name='category_add'),
    path('category/<int:category_pk>/edit/', adminapp.CategoryEdit.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', adminapp.CategoryDelete.as_view(), name='category_delete'),

    path('category/<int:category_pk>/products', adminapp.category_products, name='category_products'),
    path('category/product/<int:pk>/detail/', adminapp.ProductDetail.as_view(), name='product_detail'),
    path('category/<int:category_pk>/product/add/', adminapp.product_add, name='product_add'),
    path('category/product/<int:pk>/edit/', adminapp.product_edit, name='product_edit'),
    path('category/product/<int:pk>/delete/', adminapp.product_delete, name='product_delete'),
]

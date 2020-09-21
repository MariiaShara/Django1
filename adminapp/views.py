from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator

from adminapp.forms import AdminUserCreateForm, AdminUserEditForm, AdminClothingCategoryCreateForm, AdminClothingEditForm
from mainapp.models import ClothingCategory, Clothing




class OnlySuperUserMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['page_title'] = self.page_title,
        return data


class UsersList(OnlySuperUserMixin, PageTitleMixin, ListView):
    page_title = 'Admin/users'
    model = get_user_model()
    paginate_by = 3


@user_passes_test(lambda x: x.is_superuser)
def user_add(request):
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        form = AdminUserCreateForm()

    context = {
        'title': 'users',
        'form': form
    }

    return render(request, 'adminapp/edit_user.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_edit(request, pk):
    #user_to_edit = get_user_model().objects.filter(pk=pk).first()
    user_to_edit = get_object_or_404(get_user_model(), pk=pk)

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))

    else:
        form = AdminUserEditForm(instance=user_to_edit)

    context = {
        'page_title': 'User/edit',
        'form': form
    }

    return render(request, 'adminapp/edit_user.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    object = get_object_or_404(get_user_model(), pk=pk)

    if request.method == 'POST':
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context ={
        'page_title': 'User/delete',
        'object': object
    }

    return render(request, 'adminapp/delete_user.html', context)


class CategoriesRead(OnlySuperUserMixin, PageTitleMixin, ListView):
    page_title = 'Categories'
    model = ClothingCategory
    paginate_by = 3


class CategoryAdd(OnlySuperUserMixin, PageTitleMixin, CreateView):
    page_title = 'Category/Add'
    model = ClothingCategory
    success_url = reverse_lazy('my_admin:categories_read')
    form_class = AdminClothingCategoryCreateForm


class CategoryEdit(OnlySuperUserMixin, PageTitleMixin, UpdateView):
    page_title = 'Category/Edit'
    model = ClothingCategory
    success_url = reverse_lazy('my_admin:categories_read')
    form_class = AdminClothingCategoryCreateForm
    pk_url_kwarg = 'category_pk'


class CategoryDelete(OnlySuperUserMixin, PageTitleMixin, DeleteView):
    page_title = 'Category/Delete'
    model = ClothingCategory
    success_url = reverse_lazy('my_admin:categories_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def category_products(request, category_pk):
    category = get_object_or_404(ClothingCategory, pk=category_pk)
    object_list = category.clothing_set.all()
    context = {
        'page_title': f'Category {category.name}/products',
        'category': category,
        'object_list': object_list
    }
    return render(request, 'mainapp/clothing_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_add(request, category_pk):
    category = get_object_or_404(ClothingCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminClothingEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'my_admin:category_products',
                kwargs={'category_pk': category.pk}
            ))
    else:
        form = AdminClothingEditForm(
            initial={
                'category': category,
            }
        )

    context = {
        'page_title': 'products/add',
        'form': form,
        'category': category,
    }

    return render(request, 'adminapp/edit_product.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_edit(request, pk):
    product = get_object_or_404(Clothing, pk=pk)
    if request.method == 'POST':
        form = AdminClothingEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                 'my_admin:category_products',
                 kwargs={'category_pk': product.category.pk}
            ))
    else:
        form = AdminClothingEditForm(instance=product)

    context = {
        'page_title': 'products/edit',
        'form': form,
        'category': product.category,
        'pk': product.pk,
    }

    return render(request, 'adminapp/edit_product.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_delete(request, pk):
    product = get_object_or_404(Clothing, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse(
            'my_admin:category_products',
            kwargs={'category_pk': product.category.pk}
        ))

    context = {
        'page_title': 'products/delete',
        'category': product.category,
        'pk': product.pk,
    }

    return render(request, 'adminapp/delete_product.html', context)


class ProductDetail(OnlySuperUserMixin, PageTitleMixin, DetailView):
    page_title = 'Product/Details'
    model = Clothing



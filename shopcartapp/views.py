from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, reverse
from django.template.loader import render_to_string

from mainapp.models import Clothing
from shopcartapp.models import ShoppingCartItem


def index(request):
    #cart = ShoppingCartItem(user=request.user)
    #cart = request.user.shoppingcartitem_set.all()
    cart = request.user.shopping_bag.all()
    context = {
        'page_title': 'shopping cart',
        'cart': cart,
    }
    return render(request, 'shopcartapp/index.html', context)


@login_required
def add(request, pk):
    product = get_object_or_404(Clothing, pk=pk)
    #cart = ShoppingCartItem.objects.filter(user=request.user, product=product).first()
    cart = request.user.shopping_bag.filter(product=pk).first()
   
    if not cart:
        cart = ShoppingCartItem(user=request.user, product=product)

    cart.quantity += 1
    cart.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product', args=[pk]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, pk):
    get_object_or_404(ShoppingCartItem, pk=pk).delete()
    return HttpResponseRedirect(reverse('shopcart:index'))


def change(request, pk, quantity):
    if request.is_ajax():
        cart_item = ShoppingCartItem.objects.filter(pk=pk).first()
        if quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        context = {
            'cart': request.user.shopping_bag.all(),
        }
        result = render_to_string(
            'shopcartapp/inc/inc__shopping_bag.html',
            context=context,
            request=request,
        )

        return JsonResponse({
            'result': result,
        })






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem, Order


@login_required
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('you can not proceed to checkout page because your cart is empty.'))
        return redirect('product:product_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST, )

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )
            cart.clear()
            if not request.user.first_name:
                request.user.first_name = order_obj.first_name
            if not request.user.last_name:
                request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id
            # messages.success(request, _('your order has successfully pleased.'))
            return redirect('payment:payment_process_sandbox')

    return render(request, 'order/order_create.html', context={
        'form': order_form,
    })


@login_required()
def order_unpaid_view(request):
    user = request.user
    
    o = Order.get_number_of_paid_orders(self=request,user=user)
    if not o:
        messages.warning(request, _('order not'))
        return redirect('home')

    return render(request, 'order/unpaid_order.html', context={'order_unpaid_id': o, }, )


def order_delete_view(request, pk):
    item = get_object_or_404(Order, pk=pk)
    item.delete()
    return redirect('order_unpaid')


@login_required
def order_continue_view(request, pk):
    get_object_or_404(Order, pk=pk)
    request.session['order_id'] = pk
    return redirect('payment:payment_process_sandbox')










from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404, reverse, render
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
import re
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from allauth.account.forms import ChangePasswordForm
from cart.forms import Myaccountfrom

from .models import Product, Comment, UserFavorite,Contact_us
from .forms import CommentForms, ContactForms
from cart.forms import AddToCartProductForm




class ProductListView(generic.ListView):
    # model = Product
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(generic.DetailView):
    # model = Product
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForms()
        # context['add_to_cart_form'] = AddToCartProductForm()
        context['url_name'] = resolve(self.request.path).url_name
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForms

    def form_valid(self, form):
        # return super().form_valid(form)
        obj = form.save(commit=False)
        obj.author = self.request.user

        pk = int(self.kwargs['pk'])
        product = get_object_or_404(Product, id=pk)
        obj.product = product
        messages.success(self.request, _('Comment successfully created'))
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('product_list', )


def favorites_view(request):
    if request.user.is_authenticated:
        favorite_ = request.user.favorites.all()
    else:
        favorites = request.session.get('favorites', {})
        pk_ = [int(key) for key in favorites if re.match(r'\d+', key)]
        favorite_ = Product.objects.filter(
      id__in=pk_
    )
    return render(request, 'list_fe.html', context={'list_fe':favorite_})



def favorite_add_view(request, pk):
    if request.user.is_authenticated:
        favorite_ = get_object_or_404(Product, pk=pk)
        if not UserFavorite.objects.filter(
            user=request.user,
            product=favorite_
            ).exists():
            UserFavorite.objects.create(
            user=request.user,
            product=favorite_
            )
            messages.success(request, 'this is a success message.')
        else:
            messages.info(request, 'this is a info message.')
    else:
        favorites = request.session.get('favorites', {})
        if pk not in favorites:
            product = Product.objects.get(pk=pk)
            favorites[pk] = product.title  
            request.session['favorites'] = favorites
            messages.success(request, 'this is a success message.')
        else:
            messages.info(request, 'this is a info message.')
    return redirect(request.META['HTTP_REFERER'])


@login_required
def contact_us_view(request):
    form = ContactForms()
    last_comment = Contact_us.objects.filter(user=request.user).order_by('-created').first()
    if last_comment:
        remaining_time = (last_comment.created + timedelta(hours=12) - timezone.now()).total_seconds() / 3600
        ti = round(remaining_time, 2)
        t = f'Remaining time: { ti } hours'
    else:
        remaining_time = None
        ti = None
        t = None

    if last_comment and 0 <= ti:
        messages.warning(request, "You can only comment every {} hours".format(t))
    elif request.method == 'POST':
        form = ContactForms(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            form.save()
            messages.info(request, 'OK .')
        form = ContactForms()
    else:
        pass
    return render(request, 'contactus.html', {'form':form})




@login_required
def my_account_view(request):
    form = ChangePasswordForm()
    acco_form = Myaccountfrom()
    if request.method == 'POST':
        acco_form = Myaccountfrom(request.POST)
        if acco_form.is_valid():
            if acco_form.cleaned_data['firstname']:
                request.user.first_name = acco_form.cleaned_data['firstname']
            if acco_form.cleaned_data['lastname']:
                request.user.last_name = acco_form.cleaned_data['lastname']
            if acco_form.cleaned_data['email']:
                request.user.email = acco_form.cleaned_data['email']
            if acco_form.cleaned_data['username']:
                request.user.username = acco_form.cleaned_data['username']
            request.user.save()
    if request.user.is_authenticated:
        favorite_ = request.user.favorites.all()
    o = Order.objects.filter(user=request.user)
    
    return render(request, 'my_account.html', context={'list_fe':favorite_,'order':o, 'form':form,"acco_form":acco_form})




from .cart import Cart
from products.models import Product
import re


def cart(request):
    return {'cart': Cart(request)}
def favorite(request):

    if request.user.is_authenticated:
        favorite_ = request.user.favorites.all().count()
        
    else:
        favorite_ = len(request.session.get('favorites', {}))

    return {'favorite': favorite_}
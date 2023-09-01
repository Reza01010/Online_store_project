from django.urls import path

from .views import (order_delete_view, order_unpaid_view, order_create_view, order_continue_view)


urlpatterns = [
    path('create/', order_create_view, name='order_create'),
    path('unpaid/', order_unpaid_view, name='order_unpaid'),
    path('delete/<int:pk>/', order_delete_view, name='order_delete'),
    path('continue/<int:pk>/', order_continue_view, name='order_continue'),

]

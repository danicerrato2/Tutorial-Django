from django.urls import path
from . import views

urlpatterns = [
    path('cart_add/<slug>', views.cart_add, name='cart_add'),
    path('cart', views.cart_list, name='cart_list'),
]
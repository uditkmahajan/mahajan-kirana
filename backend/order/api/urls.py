from django.contrib import admin
from django.urls import path, include
from .views import OrderView, CartView, OrderCompleteView


urlpatterns = [
    path('order/', OrderView.as_view({
        'get' : 'getAllOrder'
    }), name = 'get all the order list'),
    
    path('order/<int:pk>/', OrderView.as_view({
        'get' : 'getOrderItems',
    }), name = 'get the items of the order'),
    
    path('cartItem/', CartView.as_view({
         'get' : 'getCartItems',
         'post' : 'addCartItem',
         'put' : 'updateCartItem',
         'delete' : 'deleteCartItem'
    }), name = 'crud operations on cart'),
    
    path('order/complete/', OrderCompleteView.as_view({
        'put' : 'orderComplete',
    }), name = 'complete the order')
]

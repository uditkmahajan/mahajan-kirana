from django.contrib import admin
from django.urls import path, include
from .views import CategoryView, ProductView, ReviewView, SnapNShop

urlpatterns = [
    path('category/',CategoryView.as_view({
        'get' : 'getCategory'
    }), name = 'get all the categories'),
    
    path('category/<str:category>/products/', ProductView.as_view({
          'get' : 'getProducts'
    }), name = 'get all the products of that category'),
    
    path('product/SnapNShop/', SnapNShop.as_view({
          'post' : 'SnapNShop'
    }), name = 'get the selected products'),
    
    path('product/<str:product>/', ProductView.as_view({
          'get' : 'getProduct'
    }), name = 'get a single product'),
    
    
    path('product/<str:product>/reviews/', ReviewView.as_view({
          'get' : 'getReviews',
          'post' : 'createReview'
    }), name = 'get all the reviews of that product and create a review'),
    
]

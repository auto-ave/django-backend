from django.urls import path

from cart.views import *

urlpatterns = [
    path('cart/getcart/', GetCart.as_view()),
    path('cart/additem/', AddItem.as_view()),
    path('cart/removeitem/', RemoveItem.as_view()),
    path('cart/clear/', ClearCart.as_view()),
    
    
    ## IRELAND URLS
    path('ie/cart/getcart/', GetCart.as_view()),
    path('ie/cart/additem/', AddItem.as_view()),
    path('ie/cart/removeitem/', RemoveItem.as_view()),
    path('ie/cart/clear/', ClearCart.as_view()),
]
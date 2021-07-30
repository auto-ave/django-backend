from django.urls import path

from cart.views import *

urlpatterns = [
    path('cart/getcart', GetCart.as_view()),
    path('cart/additem', AddItem.as_view()),
    path('cart/removeitem', RemoveItem.as_view()),
]
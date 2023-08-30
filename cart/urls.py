from django.urls import path
from cart.views import *

urlpatterns = [
path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
path('view-cart/', view_cart, name='view_cart'),  # Add this line
path('update-cart-item/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),
path('remove-from-cart-unauthenticated/<int:item_id>/', remove_from_cart_unauthenticated, name='remove_from_cart_unauthenticated'),
path('view-cart-unauthenticated/', view_cart_unauthenticated, name='view_cart_unauthenticated'),
path('update-cart-item-unauthenticated/<int:item_id>/',update_cart_item_unauthenticated, name='update_cart_item_unauthenticated'),



]

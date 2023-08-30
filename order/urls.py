from django.urls import path
from order.views import *

urlpatterns = [

path('checkout-order/', checkout, name='checkoutorder'),
path('profile/',profile,name="profile"),



]

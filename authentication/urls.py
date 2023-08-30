from django.urls import path
from authentication.views import *

urlpatterns = [
path('',index,name='index'),
path('home/',index,name='home'),
path('booktable/',booktable,name="booktable"),
path('chefs/',chefs,name='chefs'),
path('about/',about,name="about"),
path('signup/',signup, name='signup'),
path('login/',handlelogin, name='login'),
path('logout/',handlelogout,name='logout'),
    path('list/', order_list, name='order_list'),
    path('detail/<int:order_id>/', order_detail, name='order_detail'),
    path('detail/<int:order_id>/change_status/', change_order_status, name='change_order_status'),
        path('forgot-password/', send_reset_email, name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),


]


from django.urls import path
from .views import  *

urlpatterns = [
    path('admin_home/', admin_home, name='admin_home'),
    path('add_category/', add_category, name='add_category'),
    path('add_item/', add_item, name='add_item'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('edit/', admin_edit, name='admin_edit'),
    path('update/<int:item_id>/', update_item, name='update_item'),
    path('order_list/', order_list, name='orderlist'),
    path('change_order_status/<int:order_id>/', change_order_status, name='change_order_status'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),


]

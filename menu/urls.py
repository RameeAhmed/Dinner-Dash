from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from menu.views import *

urlpatterns = [
path('menu/',menu_view, name='menu'),
path('category/<str:category_name>/', category_items_view, name='category_items'),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



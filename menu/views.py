
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Item
from django.shortcuts import render, get_object_or_404




from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Item

def menu_view(request):
    categories = Category.objects.all()
    items = Item.objects.all() # Filter visible items

    paginator = Paginator(items, 6)  # 6 items per page
    page_number = request.GET.get('page')
    items_page = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'items': items_page,
    }

    return render(request, 'menu.html', context)




def category_items_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    items_from_category = Item.objects.filter(categories=category)

    context = {
        'category': category,
        'items_from_category': items_from_category,
    }
    return render(request, 'category_items.html', context)


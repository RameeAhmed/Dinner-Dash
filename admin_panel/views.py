# admin_panel/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Admin
from authentication.views import handlelogin

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Create a User instance
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create an Admin instance linked to the User
        admin = Admin(user=user)
        admin.save()

        return redirect('handlelogin')  # Redirect to login page after successful signup

    return render(request, 'admin_signup.html')  # Render the admin_signup.html template


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def admin_home(request):
    return render(request, 'admin_home.html')

from django.shortcuts import render, redirect
from django.contrib import messages

from menu.models import Category
@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = Category(name=name, description=description)
        category.save()
        messages.success(request, 'Category added successfully.')
        return redirect('admin_home')  # Redirect to admin_home or any desired page
    return render(request, 'add_category.html')


# menu/views.py
from menu.models import Item
@login_required
def add_item(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        photo = request.FILES.get('photo')
        category_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=category_ids)

        # Construct the filename: images/images/filename.ext
        filename = f'images/images/{photo.name}'

        item = Item(title=title, description=description, price=price, photo=filename)
        item.save()
        item.categories.set(categories)
        messages.success(request, 'Item added successfully.')
        return redirect('admin_home')
    return render(request, 'add_item.html', {'categories': categories})


# admin_panel/views.py
from django.shortcuts import redirect, render
from django.contrib import messages
from menu.models import Item

def delete_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        item.delete()
        messages.success(request, f"Item '{item.title}' has been deleted.")
    except Item.DoesNotExist:
        messages.error(request, "Item not found.")

    return redirect('admin_home')


from django.shortcuts import render

from django.shortcuts import render
from menu.models import Category, Item

def admin_edit(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'admin_edit.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from menu.models import Item, Category

def update_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        # Update the item attributes
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')

        # Update the visibility status
        is_visible = request.POST.get('is_visible')
        item.is_visible = is_visible == 'on'  # Checkbox returns 'on' when checked

        # Update the photo if provided
        if 'photo' in request.FILES:
            if item.photo:  # Delete the existing photo
                item.photo.delete()

            photo = request.FILES['photo']
            filename = f'images/images/{photo.name}'
            item.photo.save(filename, photo, save=False)  # Save the new photo

        item.save()

        return redirect('admin_edit')

    context = {
        'item': item,
        'categories': Category.objects.all(),
    }
    return render(request, 'update_item.html', context)

from order.models import Order,OrderItem

def change_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order = Order.objects.get(pk=order_id)
        order.status = new_status
        order.save()
        return redirect('orderlist')
    return redirect('orderlist')


def order_list(request):
    ordered_orders = Order.objects.filter(status='O')
    paid_orders = Order.objects.filter(status='P')
    completed_orders = Order.objects.filter(status='D')
    cancelled_orders = Order.objects.filter(status='C')

    editable_orders = ordered_orders | paid_orders  # Combine ordered and paid orders for editing

    context = {
        'editable_orders': editable_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
    }

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = Order.objects.get(id=order_id)

        if new_status == 'P' and order.status == 'O':
            order.status = 'P'
        elif new_status == 'D' and order.status == 'P':
            order.status = 'D'
        elif new_status == 'C' and (order.status == 'O' or order.status == 'P'):
            order.status = 'C'

        order.save()

    messages.info(request, f"Editable Orders: {editable_orders.count()}, Cancelled Orders: {cancelled_orders.count()}")

    return render(request, 'orderlist.html', context)




from django.shortcuts import render

from django.shortcuts import render

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    total_tax = sum(item.tax for item in order_items)
    total_total_value = sum(item.total_value for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'total_tax': total_tax,
        'total_total_value': total_total_value,
    }

    return render(request, 'order_detail.html', context)

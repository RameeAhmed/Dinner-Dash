

from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Process the checkout and perform necessary actions
        # ...

        # Create a new order with status 'Ordered'
        order = Order.objects.create(
            user=request.user,
            status='O',  # Set the status to 'Ordered'
        )

        # Copy cart items to order items
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                subtotal=cart_item.subtotal,
                total_value=cart_item.total_price,
                tax=cart_item.subtotal * Decimal('0.1'),
            )

        # Clear the cart and cart items
        cart_items = cart.cartitem_set.all()
        cart_items.delete()
        cart.total_price = 0
        cart.save()

        messages.success(request, 'Thank you for your order! Your order has been placed.')
        return redirect('menu')

    cart_items = cart.cartitem_set.all()
    total_quantity = sum([item.quantity for item in cart_items])
    overall_subtotal = sum([item.subtotal for item in cart_items])
    tax = overall_subtotal * Decimal('0.1')
    total_price = overall_subtotal + tax

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'overall_subtotal': overall_subtotal,
        'tax': tax,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)





from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *  # Import the Order and OrderItem models
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    paginator = Paginator(orders, per_page=5)  # Adjust per_page as needed
    page_number = request.GET.get('page')
    paginated_orders = paginator.get_page(page_number)

    context = {
        'orders': paginated_orders,
    }

    return render(request, 'profile.html', context)

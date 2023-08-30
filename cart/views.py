from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from menu.models import Item
from .models import Cart, CartItem
from decimal import Decimal
from django.contrib.auth.decorators import login_required


def remove_from_cart_unauthenticated(request, item_id):
    item_id_str = str(item_id)
    session_cart = request.session.get('cart', {})
    if item_id_str in session_cart:
        del session_cart[item_id_str]
        request.session['cart'] = session_cart
        request.session.save()

    return redirect('view_cart_unauthenticated')



from django.http import HttpResponseBadRequest
from decimal import Decimal

def update_cart_item_unauthenticated(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            return HttpResponseBadRequest("Invalid quantity")

        session_cart = request.session.get('cart', {})
        item_id_str = str(item_id)
        item_data = session_cart.get(item_id_str, {'quantity': 0, 'price': 0})

        # You should fetch the actual price of the item from your database or session,
        # wherever you are storing it for unauthenticated users
        item_price = item_data['price']

        item_data['quantity'] = quantity
        item_data['price'] = item_price  # Update the price in session data
        session_cart[item_id_str] = item_data
        request.session['cart'] = session_cart
        request.session.save()

    return redirect('view_cart_unauthenticated')



from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from cart.models import CartItem

def view_cart_unauthenticated(request):
    session_cart = request.session.get('cart', {})
    cart_items = []

    overall_subtotal = 0

    for item_id, item_data in session_cart.items():
        item = get_object_or_404(Item, id=int(item_id))  # Assuming 'Item' is your item model
        quantity = item_data.get('quantity', 0)
        price = item.price  # Retrieve price from the 'item' object
        subtotal = quantity * price
        cart_items.append(CartItem(item=item, quantity=quantity, subtotal=subtotal))
        overall_subtotal += subtotal

    tax = overall_subtotal * Decimal('0.1')
    total_price = overall_subtotal + tax

    total_quantity = sum([item_data.get('quantity', 0) for item_data in session_cart.values()])

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'overall_subtotal': overall_subtotal,
        'tax': tax,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)





from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from cart.models import Cart









def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))

        if request.user.is_authenticated:
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        else:
            if quantity > 0:
                session_cart = request.session.get('cart', {})
                item_id = str(cart_item.item.id)  # Convert the item ID to string
                session_cart[item_id]['quantity'] = quantity
                request.session['cart'] = session_cart
                request.session.save()
            else:
                item_id = str(cart_item.item.id)  # Convert the item ID to string
                session_cart = request.session.get('cart', {})
                if item_id in session_cart:
                    del session_cart[item_id]
                    request.session['cart'] = session_cart
                    request.session.save()

    return redirect('view_cart')


def remove_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
    else:
        item_id = cart_item_id
        session_cart = request.session.get('cart', {})
        if item_id in session_cart:
            del session_cart[item_id]
            request.session['cart'] = session_cart
            request.session.save()

    return redirect('view_cart')




def view_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
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

    return render(request, 'cart.html', context)

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, item=item)

        # Update the quantity instead of directly adding it
        cart_item.quantity = quantity
        cart_item.save()
    else:
        session_cart = request.session.get('cart', {})
        item_data = session_cart.get(str(item.id), {'quantity': 0, 'price': str(item.price)})  # Convert item price to string
        item_data['quantity'] += quantity
        session_cart[str(item.id)] = item_data
        request.session['cart'] = session_cart
        request.session.save()

    return redirect('menu')






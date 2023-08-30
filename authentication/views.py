from .models import UserProfile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import logout




def index(request):
    return render(request,'home.html')

def chefs(request):
    return render(request,'chefs.html')

def booktable(request):
    return render(request,'booktable.html')


def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method == "POST":
        display_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, 'signup.html')

        try:
            if UserProfile.objects.get(email=email):
                messages.info(request, "Email is already taken")
                return render(request, 'signup.html')
        except UserProfile.DoesNotExist:
            pass

        user = UserProfile.objects.create_user(display_name, email, password)
        user.is_active = True  # Setting user as inactive initially
        user.save()

        # You can also authenticate and login the user here
        # authenticate() checks the username and password
        # login(request, user)

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, "signup.html")




def handlelogout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page or any other desired page


def authenticate_and_login(request, email, password):
    print("Email:", email)
    print("Password:", password)
    user = authenticate(username=email, password=password)  # Use email for authentication
    if user is not None:
        if user.is_active:  # Check if the user is active
            login(request, user)
            return True
        else:
            messages.error(request, "Your account is inactive. Contact support for assistance.")
    return False

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect




from django.shortcuts import render
from order.models import Order


from django.shortcuts import render, get_object_or_404

def transfer_cart_items(request, user):
    anonymous_cart = request.session.get('cart', {})
    authenticated_cart = user.cart.get_cart_data()

    for item_id, quantity in anonymous_cart.items():
        authenticated_cart[item_id] = authenticated_cart.get(item_id, 0) + quantity

    # Clear anonymous cart
    request.session['cart'] = {}

    # Update authenticated cart
    user.cart.update_cart(authenticated_cart)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from cart.models import Cart, CartItem

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from cart.models import Cart, CartItem
from menu.models import Item

def handlelogin(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                # Retrieve or create a cart for the logged-in user
                cart, created = Cart.objects.get_or_create(user=user)

                # If the user had items in the session cart, transfer them to the user's cart
                if 'cart' in request.session:
                    session_cart = request.session['cart']
                    for item_id_str, item_data in session_cart.items():
                        item_id = int(item_id_str)
                        item = Item.objects.get(id=item_id)
                        quantity = item_data.get('quantity', 0)

                        if quantity > 0:
                            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
                            cart_item.quantity = quantity
                            cart_item.save()

                    del request.session['cart']  # Clear session cart data

                if user.is_superuser:
                    messages.success(request, "Welcome Admin!")
                    return redirect('admin_home')
                else:
                    messages.success(request, "Login Success")
                    return redirect('index')
            else:
                messages.error(request, "Your account is inactive. Contact support for assistance.")
        else:
            messages.error(request, "Invalid Credentials")

    return render(request, 'login.html')


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'order_detail.html', context)

# orders/views.py

from django.shortcuts import render, redirect
from order.models import Order
from django.contrib.auth.decorators import login_required

@login_required
def order_list(request):
    completed_orders = Order.objects.filter(status='C').order_by('-created_at')
    waiting_orders = Order.objects.filter(status='W').order_by('-created_at')

    context = {
        'completed_orders': completed_orders,
        'waiting_orders': waiting_orders,
    }

    return render(request, 'order_list.html', context)

@login_required
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'W':
        order.status = 'C'
        order.save()
    return redirect('order_list')

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def send_reset_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = UserProfile.objects.get(email=email)

        # Generate a token for password reset
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Build the password reset link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"

        # Send the password reset email
        subject = "Password Reset Request"
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(subject, message, 'noreply@localhost', [email])

        return render(request, 'password_reset_sent.html')

    return render(request, 'forgot_password.html')


from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from .models import UserProfile

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from .models import UserProfile

def reset_password(request, uidb64, token):
    """
    View to handle the password reset process.
    """
    try:
        # Decode the user ID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()

        # Get the user associated with the user ID
        user = UserProfile.objects.get(pk=uid)

        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                confirm_new_password = request.POST.get('confirm_new_password')

                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    user.save()

                    # Update the user's session to reflect the new password
                    update_session_auth_hash(request, user)

                    return redirect('login')  # Redirect to the login page
                else:
                    return render(request, 'reset_password_form.html', {'user': user, 'error_message': 'Passwords do not match'})
            else:
                return render(request, 'reset_password_form.html', {'user': user})
        else:
            return render(request, 'reset_password_invalid.html')
    except UserProfile.DoesNotExist:
        return render(request, 'reset_password_invalid.html')


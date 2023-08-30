# cart/models.py
from django.conf import settings
from django.db import models
from menu.models import Item
from django.utils import timezone  # Import datetime module
from datetime import datetime  # Import datetime module
from decimal import Decimal



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_cart_data(self):
        cart_items = CartItem.objects.filter(cart=self)
        cart_data = {str(item.item.id): item.quantity for item in cart_items}
        return cart_data

    def update_cart(self, cart_data):
        CartItem.objects.filter(cart=self).delete()
        for item_id, quantity in cart_data.items():
            item = Item.objects.get(id=item_id)
            CartItem.objects.create(cart=self, item=item, quantity=quantity)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add the tax field
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_subtotal(self):
        return self.item.price * self.quantity

    def save(self, *args, **kwargs):
        self.subtotal = self.item.price * self.quantity
        self.tax = self.subtotal * Decimal('0.1')  # Calculate tax
        self.total_price = self.subtotal + self.tax  # Calculate total_price including tax
        super().save(*args, **kwargs)

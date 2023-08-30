from django.db import models

# menu/models.py
from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=False)  # Cannot be empty
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    photo = models.ImageField(upload_to='images/images', null=True, blank=True)
    categories = models.ManyToManyField(Category)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

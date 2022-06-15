from django.db import models
from django.core.validators import RegexValidator

from catalog.models import Book

class Order(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=5,
        validators=[RegexValidator(r'[0-9]{5}')])
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["updated"]

    def __str__(self):
        return f'{self.id}, {self.last_name}, {self.first_name}'

    def get_total_cost(self):
        total = 0.0
        for item in list(self.items.all()):
            total += float(item.price * item.quantity)

        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
        related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
        related_name="book")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id}, {self.book}'
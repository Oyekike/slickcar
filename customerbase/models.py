from django.db import models
from django.contrib.auth.models import User
from home.models import Product

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    pix = models.ImageField(upload_to='customer', default='customer/avatar.png', blank=True, null=True)

    def __str__(self):
        return self.user.username 
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    paid = models.BooleanField()
    amount = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username 
    
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    paid = models.BooleanField()
    phone = models.CharField(max_length=50)
    pay_code = models.CharField(max_length=50)
    additional_info = models.TextField()
    purchase_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
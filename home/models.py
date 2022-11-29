from django.db import models

# Create your models here.

class AppInfo(models.Model):
    name = models.CharField(max_length=50)
    carousel1 = models.ImageField(upload_to='carousel')
    carousel2 = models.ImageField(upload_to='carousel')
    carousel3 = models.ImageField(upload_to='carousel')
    banner = models.ImageField(upload_to='banner')
    logo = models.ImageField(upload_to='logo')
    avatar = models.ImageField(upload_to='dp')
    copyright = models.IntegerField()

    def __str__(self): 
        return self.name
    
class Category(models.Model):
    brand = models.CharField(max_length=50)
    pix = models.ImageField(upload_to='brandpix')
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.brand

class Product(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    year = models.IntegerField()
    seats = models.IntegerField()
    price = models.IntegerField()
    picture = models.ImageField(upload_to='carpix')
    registered = models.BooleanField()
    uploaded_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
       return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=70)
    message = models.TextField()
    sent = models.TimeField(auto_now_add=True)

    def __str__(self):
       return self.name



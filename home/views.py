import uuid
import json
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db.models import Q 
from customerbase.forms import CustomerForm, ProfileForm
from customerbase.models import *
from home.forms import ContactForm
from . models import *

# Create your views here.

def index(request):
    info = AppInfo.objects.get(pk=1)
    cat = Category.objects.all()

    context = {
        'info' :info,
        'cat' : cat,
    }

    return render(request, 'index.html', context)

def product(request):
    carproducts = Product.objects.all()
    p = Paginator(carproducts, 8)
    page = request.GET.get('page')
    pagin = p.get_page(page)

    context = {
        'pagin':pagin,
    }
    return render(request, 'products.html', context)

def category(request, id, slug):
    categ = Category.objects.get(pk=id)
    carbrand = Product.objects.filter(type_id=id)

    context = {
        'categ':categ,
        'carbrand':carbrand
    }

    return render(request, 'category.html', context)

def detail(request, id, slug):
    cardet = Product.objects.get(pk=id)

    context = {
        'cardet':cardet,
    }

    return render(request,'detail.html', context)

def contact(request):
    contact = ContactForm()
    if request.method == 'POST':
        contact = ContactForm(request.POST)
        if contact.is_valid():
            contact.save()
            messages.success(request, 'your message has been sent successfully')
            return redirect('home')

    context = {
        'contact':contact 
    }

    return render(request, 'contact.html', context)

def signout(request):
    logout(request)
    messages.success(request, 'you are now signed out')
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'sign in successful')
            return redirect('home')
        else:
            messages.info(request, 'username/password is incorrect')

    return render(request, 'login.html')

def register(request):
    form = CustomerForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        pix = request.POST['pix']
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save()
            newuser = Customer(user=user)
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.email = user.email 
            newuser.phone = phone
            newuser.address = address
            newuser.pix = pix 
            newuser.save()
            messages.success(request, f'congratulations {user.username} your account is created successfully')
            return redirect('signin')
        else:
            messages.error(request, form.errors)

    return render(request, 'register.html')

@login_required(login_url='signin')
def profile(request):
    userprof = Customer.objects.get(user__username = request.user.username)

    context = {
        'userprof':userprof
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    form = ProfileForm(instance=request.user.customer)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            user = form.save()
            new = user.first_name.title()
            messages.success(request, f'Dear {new} your profile is now updated')
            return redirect('profile')
        else:
            new = user.first_name.title()
            messages.error(request, f'Dear {new} your profile update generated the following errors: {form.errors}')
            return redirect('profile_update')

    context = {
        'userprof':userprof
    }

    return render(request, 'profile_update.html', context)

@login_required(login_url='signin')
def password_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        new = request.user.username.title()
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Dear {new} your password change is successful')
            return redirect('profile')
        else:
            messages.error(request, f'Dear {new} a problem occured with the following errors: {form.errors}')
            return redirect('password_update')
    
    context = {
        'userprof':userprof,
        'form':form,
    }

    return render(request, 'password_update.html', context)

@login_required(login_url='signin')
def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        car = request.POST['carid']
        main = Product.objects.get(pk=car)
        cart = Cart.objects.filter(user__username = request.user.username, paid=False)
        if cart:
            basket = Cart.objects.filter(user__username = request.user.username, paid=False, car = main.id, quantity=quantity).first()
            if basket:
                basket.quantity += quantity
                basket.amount = main.price * basket.quantity 
                basket.save()
                messages.success(request, 'one item added to cart')
                return redirect('products')
            else:
                newitem = Cart()
                newitem.user = request.user 
                newitem.car = main 
                newitem.quantity = quantity
                newitem.price = main.price 
                newitem.amount = main.price * quantity 
                newitem.paid = False 
                newitem.save()
                messages.success(request, 'one item added to cart')
                return redirect('products')
        else:
            newcart = Cart()
            newcart.user = request.user 
            newcart.car = main
            newcart.quantity = quantity 
            newcart.price = main.price 
            newcart.amount = main.price * quantity 
            newcart.paid = False 
            newcart.save()
            messages.success(request, 'one item added to cart')
            return redirect('products')

@login_required(login_url='signin')
def cart(request):
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.quantity 
        item.save()

    subtotal = 0 
    vat = 0
    total = 0 

    for item in cart:
        subtotal += item.price * item.quantity 
        vat = 0.075 * subtotal 
        total = subtotal + vat

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total 
    }

    return render(request, 'cart.html', context)

@login_required(login_url='signin')
def delete(request):
    if request.method == 'POST':
        del_item = request.POST['del_id']
        Cart.objects.filter(pk=del_item).delete()
        messages.success(request, 'one item deleted')
        return redirect('cart')

@login_required(login_url='signin')
def increase(request):
    if request.method == 'POST':
        qty_item = request.POST['quantid']
        new_qty = request.POST['quant']
        newqty = Cart.objects.get(pk=qty_item)
        newqty.quantity = new_qty
        newqty.amount = newqty.price * newqty.quantity
        newqty.save()
        messages.success(request, 'quantity updated')
        return redirect('cart')

def checkout(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid = False)
    for item in cart:
        item.amount = item.price * item.quantity
        item.save()

    subtotal = 0 
    vat = 0
    total = 0 

    for item in cart:
        subtotal += item.price * item.quantity
        vat = 0.075 * subtotal
        total = subtotal + vat 

    context = {
        'userprof':userprof,
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total 
    }

    return render(request, 'checkout.html', context)

def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_993b219f003efede471243f80d005eb7b2a6c8de' #secret key from paystack
        curl = 'https://api.paystack.co/transaction/initialize' #paystack call url 
        cburl = 'http://44.204.81.61/callback' #payment confirmation page 
        ref = str(uuid.uuid4()) #reference id required by paystack as an additional order number 
        profile = Customer.objects.get(user__username = request.user.username)
        order_no = profile.id #main order number 
        total = float(request.POST['total']) * 100 #total amount to be charged from customer card
        user = User.objects.get(username = request.user.username) #query the model for customer details
        email = user.email #save customer email to send to paystack 
        first_name = request.POST['first_name'] #collect from the template incase there is a change
        last_name = request.POST['last_name'] #collect from the template incase there is a change
        additional_info = request.POST['add_info'] #collect from the template incase there is a change
        phone = request.POST['phone'] #collect from the template incase there is a change

        #collect data to send to paystack via call 
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':ref, 'amount':int(total), 'email':user.email, 'callback_url':cburl, 'order_number':order_no, 'currency':'NGN'}

        #make a call to paystack 
        try:
            r = requests.post(curl, headers=headers, json=data) #pip install requests
        except Exception:
            messages.error(request, 'network busy, try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Purchase()
            account.user = user 
            account.first_name = user.first_name 
            account.last_name = user.last_name 
            account.amount = total/100 
            account.paid = True 
            account.phone = phone
            account.pay_code = ref 
            account.additional_info = additional_info
            account.save() 

            return redirect(rdurl)

    return redirect('checkout')

def callback(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid = False)

    for item in cart:
        item.paid = True 
        item.save()

        car = Product.objects.get(pk=item.car.id)

    context = {
        'userprof':userprof,
        'cart':cart,
        'car':car
    }

    return render(request, 'callback.html', context)

def search(request):
    if request.method == 'POST':
        items = request.POST['search']
        searched = Q(Q(name__icontains=items)| Q(model__icontains=items)| Q(year__icontains=items))
        searched_item = Product.objects.filter(searched)

        context = {
            'items':items,
            'searched_item':searched_item
        }

        return render(request, 'search.html', context)
    
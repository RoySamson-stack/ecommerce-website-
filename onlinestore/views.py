from django.shortcuts import render
from django.http import HttpResponse
#import request from django.http
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import  *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
import json 
from .forms import CreateUserForm, LoginForm
from .utils import cookieCart, cartData, guestOrder


# Create your views here.
def index(request):
    products = Product.objects.all()
   #get cart data from cartData
   
    data = {
            'products': products[0:6]
                
            } 
    return render(request, 'onlinestore/index.html', data)


def login_view(request,):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return render(request, 'onlinestore/login.html')
    context = {}
    return render(request, 'onlinestore/login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')

def signup(request):
   form = CreateUserForm()
   if request.method == 'POST':
         form = CreateUserForm(request.POST)
         if form.is_valid():
            form.save()
            return redirect('login')
            messages.success(request, 'Account created successfully')     
   else:
         form = CreateUserForm()
         
   return render(request, 'onlinestore/signup.html', {'form': form})    



            
def products(request):
    products = Product.objects.all()
    #get the cart data from the cart Fuct
    
    context = {
        'products': products
    }
    return render(request, 'onlinestore/products.html', context)



def product_view(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'onlinestore/product_view.html', {'product': product})


#create the add to cart view 
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    # quantity = int(request.POST.get('quantity'))
    order, created = Cart.objects.get_or_create( purchase_complete=False)
    orderItem, created = CartItems.objects.get_or_create(product=product, cart=order)
    orderItem.save()
    return redirect('cart')

def remove_from_cart(request, id):
    customer = request.user.username
    product = Product.objects.get(id=id)
    order, created = Cart.objects.get_or_create(customer=customer, purchase_complete=False)
    orderItem, created = CartItem.objects.get_or_create(product=product, order=order)
    orderItem.delete()
    return redirect('cart')


#create a view to clear cart 
def clear_cart(request):
    customer = request.user.username
    order, created = Cart.objects.get_or_create(purchase_complete=False)
    cartItems = CartItems.objects.filter(cart=order)
    cartItems.delete()
    return redirect('cart')    
    
    
    
    
    
    
    
#create the cart view
def cart(request):
    customer = request.user.username
    order, created = Cart.objects.get_or_create(purchase_complete=False)
    cartItems = CartItems.objects.filter(cart=order)
    context = {
        'cartItems': cartItems,
    }
    return render(request, 'onlinestore/cart.html', context)



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


def product_view(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'onlinestore/product_view.html', {'product': product})




def cart(request):
    return render(request, 'onlinestore/cart.html')

def products(request):
    products = Product.objects.all()
    #get the cart data from the cart Fuct
    
    context = {
        'products': products
    }
    return render(request, 'onlinestore/products.html', context)

#create the cart view 
#find a way to push the cart content to the database then pull i ttp the frontend
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.username
    product = Product.objects.get(id=productId)
    
    order, created = Cart.objects.get_or_create(customer=customer, purchase_complete=False)
    orderItem , created = CartItem.objects.get_or_create(product=product, order=order)
    
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1) 
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added to cart', safe=False)       
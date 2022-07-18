from django.shortcuts import render
from django.http import HttpResponse
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
   username=''
   form = CreateUserForm()
   if request.method == 'POST':
         form = CreateUserForm(request.POST)
         if form.is_valid():
            form.save()
            return redirect('login')
            messages.success(request, 'Account created successfully')     
   else:
         form = CreateUserForm()
   try :
        user = User.objects.get(username=username)
        context = {'form': form, 'user': user, 'error_message': 'Username already exists'}
        messages.error(request, 'Username has already been taken')
        return render(request, 'onlinestore/signup.html', context)
   except User.DoesNotExist:
        context = {'form': form}
        return render(request, 'onlinestore/signup.html', context)     
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

def cart_id(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is None:
        cart_id = uuid4().hex[:10]
        request.session['cart_id'] = cart_id
    return cart_id


#create the add to cart view 
def add_to_cart(request, id, quantity=0):
    if request.user.is_anonymous:
        customer = None 
        product = Product.objects.get(id=id)
        order, created = Cart.objects.get_or_create(customer=customer, purchase_complete=False)
        orderItem, created = CartItems.objects.get_or_create(product=product, cart=order)
        if orderItem is not None:
            quantity += 1
            orderItem.save()
        else:    
            orderItem.save()
    else:     
        customer = request.user
        product = Product.objects.get(id=id)
        order, created = Cart.objects.get_or_create(customer=customer, purchase_complete=False)
        orderItem, created = CartItems.objects.get_or_create(product=product, cart=order)
        if orderItem is not None:
            quantity += 1
            orderItem.save()
        else:    
            orderItem.save()      
    return redirect('products')

#create a view to clear cart 
def clear_cart(request):
    customer = request.user
    order, created = Cart.objects.get_or_create(purchase_complete=False)
    cartItems = CartItems.objects.filter(cart=order)
    cartItems.delete()
    return redirect('cart')    



#remove cart item from cart using view
def remove_cart_item(request, id):
    customer = request.user
    product = Product.objects.get(id=id)
    order = Cart.objects.filter( customer=customer)
    orderItem = CartItems.objects.filter(product=product, cart__in=order)
    orderItem.delete()
    return redirect('cart')
#create the cart view

def cart(request):
    customer = request.user
    order = Cart.objects.filter(customer=customer, purchase_complete=False)
    cartItems = CartItems.objects.filter(cart__in=order)
    item_count = cartItems.count()
    context = {
        'cartItems': cartItems,
        'item_count': item_count,
    }
    return render(request, 'onlinestore/cart.html', context)

#create a checkout view that will be used to create the order
def checkout(request):
    customer = request.user
    order = Cart.objects.filter(customer=customer)
    order.purchase_complete = True
    cartItems = CartItems.objects.filter(cart__in=order)
    context = {
        'cartItems': cartItems,
        'order': order
    }
    return render(request, 'onlinestore/checkout.html', context)

#create add to cart view using django and check if item is already in cart it just add the qunatity to the cart


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
from django.db.models import F, Sum

from django.core.paginator import Paginator





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
    
    
    #set up pagination
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    products_pages = paginator.get_page(page)
    context = {
        'products': products,
        'products_pages': products_pages
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


def add_to_cart(request, id, quantity=0):
    if request.user.is_anonymous:
        customer = None 
        product = Product.objects.get(id=id)
        # quantity = int(request.POST.get('quantity', 1))
        print(quantity)
        order, created = Cart.objects.get_or_create(customer=customer, purchase_complete=False)
        orderItem, created = CartItems.objects.get_or_create(product=product, cart=order)
     #check if the item exist in the cart 
        
    else:     
        customer = request.user
        product = Product.objects.get(id=id)
        order, created = Cart.objects.get_or_create(customer=customer, purchase_complete=False)
        orderItem, created = CartItems.objects.get_or_create(product=product, cart=order)
        # if orderItem is not None:
        #     quantity += 1
        #     orderItem.save()
        # else:    
        #     orderItem.save() 
        context = {'orderItem': orderItem, 'quantity': quantity}   
    itemexist = CartItems.objects.filter(product=product, cart=order).exists()
    if itemexist:
            cart = CartItems.objects.filter(product=product, cart=order)
            orderItem.quantity += 1
            orderItem.total = orderItem.quantity * orderItem.product.price
            orderItem.save()
    return redirect('products')

def clear_cart(request):
    customer = request.user
    order, created = Cart.objects.get_or_create(customer=customer, purchase_complete=False)
    cartItems = CartItems.objects.filter(cart=order)
    cartItems.delete()
    return redirect('cart')    


# def update_cart(request):
#     customer = request.user
#     order = Cart.objects.filter(customer=customer)

    
def remove_cart_item(request, id):
    customer = request.user
    product = Product.objects.get(id=id)
    order = Cart.objects.filter( customer=customer)
    orderItem = CartItems.objects.filter(product=product, cart__in=order)
    orderItem.delete()
    return redirect('cart')

def cart(request, total = 0, quantity=0, itemtotal = 0):
    customer = request.user
    choice = request.POST.get('choice', None)
    order = Cart.objects.filter(customer=customer, purchase_complete=False)
    cartItems = CartItems.objects.filter(cart__in=order)
    item_count = cartItems.count()
    # quantity = int(request.POST.get('quantity', 1))
    for cartItem in cartItems:
        itemtotal = int(cartItem.quantity * cartItem.product.price)
    for item in cartItems:
        total += (int(item.total))
    # if choice in ['1500']:
    #       total += 1500
    # elif choice in ['2500']:
    #     total += 2500
    # elif choice in ['3500']:
    #     total += 3500       
    # elif choice in ['0']:
    #     total += 0 
    context = {
        'cartItems': cartItems,
        'item_count': item_count,
        # 'itemtotal': itemtotal,
        'total': total,
        # 'grandTotal': grandTotal
        
    }
    return render(request, 'onlinestore/cart.html', context)

def checkout(request, total=0):
    customer = request.user
    order = Cart.objects.filter(customer=customer)
    order.purchase_complete = True
    cartItems = CartItems.objects.filter(cart__in=order)
    #reduce the quantity in stck for products after purchase 
    for item in cartItems:
        product = Product.objects.get(id=item.product.id)
        total += (int(item.total))
        product.inventory -= item.quantity
        product.save()
    context = {
        'cartItems': cartItems,
        'order': order,
        'total': total
    }

    order = Cart.objects.filter(customer=customer)
    customer = request.user
    shipping_country = request.POST.get('country')
    shipping_address = request.POST.get('address')
    shipping_city =request.POST.get('city')
    shipping_zipcode = request.POST.get('postcode')
    shipping_county = request.POST.get('county')
    shipping_town = request.POST.get('city')
    phone = request.POST.get('phone_number')
    email = request.POST.get('email')
    order_complete = True 
    payment_complete = True
    checkout = Checkout.objects.create(
        customer=customer,
        shipping_country = shipping_country,
        shipping_address = shipping_address,
        shipping_city = shipping_city,
        shipping_zipcode = shipping_zipcode,
        shipping_county = shipping_county,
        shipping_town = shipping_town,
        phone_number = phone,
        order_complete = order_complete,
        payment_complete = payment_complete
        
    )
    checkout.save()
    return render(request, 'onlinestore/checkout.html', context)

    
     
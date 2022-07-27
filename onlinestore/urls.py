from django.urls import path, include,re_path
from django.contrib.auth.decorators import login_required
from . import views
from .views import * 
from django.conf.urls.static import static




urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.login_view, name='login'),
  path("signup/", views.signup, name="signup"),
  path("logout/", views.logout_view, name="logout"), 
  path('cart/', login_required(views.cart, login_url='/login/'), name='cart'),
  path('cart/add/<int:id>', views.add_to_cart, name='add_to_cart'),
  path('cart/remove_item/<int:id>/', views.remove_cart_item, name='remove_cart_item'),
  path('cart/update_cart/', views.update_cart, name='update_cart'),
  path('cart/clear', views.clear_cart, name='clear_cart'),
  path('checkout/', login_required(views.checkout, login_url="/login/"), name='checkout'),
  path('cart/add_quantity/<int:id>/', views.add_quantity, name='add_quantity'),
  path('cart/remove_quantity/<int:id>/', views.remove_quantity, name='remove_quantity'),
  path('products/', views.products, name='products'),
  path('product/<int:id>/', views.product_view, name='product_view'),
]
from django.urls import path, include,re_path
from django.contrib.auth.decorators import login_required
from . import views
from .views import * 




urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.login_view, name='login'),
  path("signup/", views.signup, name="signup"),
  path("logout/", views.logout_view, name="logout"),
  path('cart/', views.cart, name='cart'),#return the login required 
  path('products/', views.products, name='products'),
  path('product/<int:id>/', views.product_view, name='product_view'),
  path('update_item/',views.updateItem, name='update-item'),
]
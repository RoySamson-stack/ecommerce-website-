from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Collection)
admin.site.register(Customer)
admin.site.register(CartItems)
admin.site.register(Cart)
admin.site.register(Checkout)

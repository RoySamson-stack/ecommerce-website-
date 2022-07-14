from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
  first_name = models.CharField(max_length=200, null=True)
  username = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200)
  password = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.username
  
  
class Collection(models.Model):
  title = models.CharField(max_length=200, null=True)
  description = models.CharField(max_length=200, null=True)
  gender = models.CharField(max_length=200, null=True)
  
  def __str__(self):
    return self.title


#product model
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField()
    price = models.FloatField(null=True)
    description = models.CharField(max_length=1000, null=True)
    inventory = models.IntegerField(null=True)
    Collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(max_length=200, null=True, blank=True , upload_to="images/")
    filter = models.CharField(max_length=200,  null=True)
    class Meta:
      ordering = ['name']
      index_together = [
        ['id', 'slug']
      ]

    def __str__(self):
        return self.name
      
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    def get_absolute_url(self):
         return reverse('onlinestore:product_view', args=[self.id, self.slug])

   
#cart model          
class Cart(models.Model):
  customer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  purchase_complete = models.BooleanField(default=False)
  transaction_id = models.CharField(max_length=200, null=True)
  order_date = models.DateTimeField(auto_now_add=True, null=True)
   
   
  def __str__(self):
    return str(self.id)
  
    @property
    def shipping(self):
      shipping = False
      cartitems = self.cartitem_set.all()
      for i in cartitems:
        if i.product.digital == False:
          shipping = True
      return shipping

    @property
    def get_cart_total(self):
      cartitems = self.cartitem_set.all()
      total = sum([item.get_total for item in cartitems])
      return total 

    @property
    def get_cart_items(self):
      cartitems = self.cartitem_set.all()
      total = sum([item.quantity for item in cartitems])
      return total 


      
    
  
#cart items model 
class  CartItems(models.Model):
  #can use the uuid for the primary key
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
  is_ordered = models.BooleanField(default=False)
  quantity = models.IntegerField(null=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  
  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total
  #onlcik the the items as cart items  
  
  
  
  
#create the payment model 
#delivery model 
class Delivery(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    county = models.CharField(max_length=200, null=False)
    street = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
  
  
  

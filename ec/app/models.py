from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATE_CHOICES = (
    ('Ras Jebel', 'Ras Jebel'),
    ('Rafraf', 'Rafraf'),
    ('Matline', 'Matline'),
    ('Ariana', 'Ariana'),
    ('Beja', 'Beja'),
    ('Ben Arous', 'Ben Arous'),
    ('Bizerte', 'Bizerte'),
    ('Gabes', 'Gabes'),
    ('Gafsa', 'Gafsa'),
    ('Jendouba', 'Jendouba'),
    ('Kairouan', 'Kairouan'),
    ('Kasserine', 'Kasserine'),
    ('Kebili', 'Kebili'),
    ('Kef', 'Kef'),
    ('Mahdia', 'Mahdia'),
    ('Manouba', 'Manouba'),
    ('Medenine', 'Medenine'),
    ('Monastir', 'Monastir'),
    ('Nabeul', 'Nabeul'),
    ('Sfax', 'Sfax'),
    ('Sidi Bouzid', 'Sidi Bouzid'),
    ('Siliana', 'Siliana'),
    ('Sousse', 'Sousse'),
    ('Tataouine', 'Tataouine'),
    ('Tunis', 'Tunis'),
    ('Zaghouan', 'Zaghouan'),
    ('Sidi Thabet', 'Sidi Thabet'),
    ('Marsa', 'Marsa'),
    ('La Manouba', 'La Manouba'),
    ('El Hamma', 'El Hamma'),
    ('Hammamet', 'Hammamet'),
    ('El Kef', 'El Kef'),
    ('Médina', 'Médina'),
    ('Carthage', 'Carthage'),
    ('La Soukra', 'La Soukra'),
    ('El Mourouj', 'El Mourouj'),
    ('El Aouina', 'El Aouina'),
    ('Tebourba', 'Tebourba'),
    ('Mornaguia', 'Mornaguia'),
    ('Oued Ellil', 'Oued Ellil'),
    ('Mahares', 'Mahares'),
    ('Nabeul', 'Nabeul'),
    ('El Menzah', 'El Menzah'),
    ('Sidi Hassine', 'Sidi Hassine'),
    ('Grombalia', 'Grombalia'),
)


CATEGORY_CHOICES=(
    ('DW','DRESS WATHCES'),
    ('SM','SMART WATCHES'),
    ('SW','SPORT WATCHES'),
    ('AW','AUTOMATIC WATCHES'),
    ('CW','CHRONOGRAPH WATCHES'),
    ('DV','DIVING WATCHES'),
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=20)
    product_image=models.ImageField(upload_to='product')
    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
     ('Accepted', 'Accepted'),
     ('Packed', 'Packed'),
     ('On The Way', 'On The Way'),
     ('Delivered', 'Delivered'),
     ('Cancel', 'Cancel'),
     ('Pending', 'Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True) 
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False) 


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price  # Fixed total cost calculation
    
class Wishlist(models.Model):
    user =models. ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


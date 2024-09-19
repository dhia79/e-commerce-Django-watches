from django.shortcuts import render,redirect
from django.views import View
from .models import Cart, Customer, Payment, Product,OrderPlaced,Wishlist,User
from .forms import CustomerRegistrationForm, CustomerProfileForm,User
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q,Count
import razorpay
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django. contrib.auth.decorators import login_required
from django. utils. decorators import method_decorator
from .models import Product, Wishlist


# Create your views here.
@login_required
def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    return render(request, "app/home.html")
   
@login_required    
def about(request):
    totalitem = 0
    wishitem=0

    if request.user.is_authenticated:
        totalitem =len(Cart.objects.filter(user=request.user))
        Wishitem =len(Wishlist.objects.filter(user=request.user))

    return render(request, "app/about.html",locals())

@login_required
def contact(request):
    wishitem=0
    totalitem =0
    if request. user.is_authenticated:
        totalitem = len (Cart.objects.filter(user=request.user))
        Wishitem =len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len (Cart.objects.filter(user=request.user))
            Wishitem =len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())

@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len (Cart.objects.filter(user=request.user))
            Wishitem =len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/category.html", locals())

@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist= Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len (Cart.objects.filter(user=request.user))
            Wishitem =len(Wishlist.objects.filter(user=request.user))
        wishlist= Wishlist.objects.filter(Q(product=product) & Q(user=request.user))

        return render(request, "app/productdetail.html", locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html',locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        form = CustomerProfileForm()
        totalitem =0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully") 
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html', locals())

# The address function should be outside of any class
@login_required
def address(request):
    add = Customer.objects. filter(user=request.user)
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len (Cart.objects. filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))  
    return render(request,'app/address.html',locals())
    
@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")
    
@login_required
def add_to_cart(request):
    user = request.user
    if request.method == 'POST':
        product_id = request.POST.get('prod_id')  # Fetch prod_id from POST data
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price 
        amount = amount + value
    totalamount = amount + 40
    totalitem=0
    wishlist=0

    if request.user.is_authenticated:
        totalitem = len (Cart.objects. filter(user=request.user))
        wishitem = len(Wishlist.objects. filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user  # Corrected the typo
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    # Fetch the wishlist products for the current user
    wishlisted_products = Wishlist.objects.filter(user=user).select_related('product')

    # Pass data to the template
    context = {
        'wishlisted_products': [wishlist.product for wishlist in wishlisted_products],
        'totalitem': totalitem,
        'wishitem': wishitem
    }

    return render(request, "app/wishlist.html", context)

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request. user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects. filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)

        cart_items=Cart.objects.filter(user=user)
        famount= 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount=int (totalamount*100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount,"currency": "INR","receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        #{'amount': 9200, 'amount_due': 9200, 'amount_paid': 0, 'attempts': 0, 'created_at': 1725578660, 'currency': 'INR', 'entity': 'order', 'id': 'order_OtfJDAtgiQFalE', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'}
        order_id = payment_response  ['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'app/checkout.html',locals())

@login_required
def orders(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart. objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)  # Fetch orders for the logged-in user
    context = {
        'order_placed': order_placed
    }
    return render(request, 'app/orders.html', context)

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user

    # Fetch the customer and payment records
    customer = get_object_or_404(Customer, id=cust_id)
    payment = get_object_or_404(Payment, razorpay_order_id=order_id)

    # Update payment status and payment ID
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    # Save order details
    cart_items = Cart.objects.filter(user=user)
    for c in cart_items:
        OrderPlaced(
            user=user,
            customer=customer,
            product=c.product,  # Fixed the field name
            quantity=c.quantity,
            payment=payment
        ).save()
        c.delete()

    return redirect("orders")




def plus_cart(request):
    if request. method == 'GET' :
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40

        #print (prod_id)
        data={
            'quantity':c.quantity,
            'amount' : amount,
            'totalmamount':totalamount

        }
    return JsonResponse(data)
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity > 1:  # Only reduce quantity if it's greater than 1
            c.quantity -= 1
            c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def plus_wishlist(request, product_id):
    if request.method == 'POST':  # Use POST instead of GET as you're sending POST requests
        product = Product.objects.get(id=product_id)  # Use product_id directly
        user = request.user
        # Add the product to the wishlist
        Wishlist.objects.get_or_create(user=user, product=product)  # Prevent duplicate entries
        data = {'message': 'Wishlist Added Successfully'}
        return JsonResponse(data)


def minus_wishlist(request, product_id):
    # Your logic for removing the product from the wishlist
    product = Product.objects.get(id=product_id)
    user = request.user
    wishlist_item = Wishlist.objects.filter(user=user, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
    return JsonResponse({'message': 'Wishlist Item Removed Successfully'})


@login_required 
def search(request):
    query = request.GET.get('search', '')
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    products = Product.objects.filter(title__icontains=query)  # 'icontains' is used for case-insensitive search
    
    return render(request, 'app/search.html', {'query': query, 'products': products, 'totalitem': totalitem, 'wishitem': wishitem})


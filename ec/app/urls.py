from django.urls import path  # Corrected: 'ur1s' to 'urls'
from . import views  # Corrected: 'import' to '.'
from django.conf import settings
from django.conf.urls.static import static  # Corrected: 'conf urls' to 'conf.urls'
from django.contrib.auth import views as auth_views 
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from .views import Checkout
from django.contrib import admin
from .views import show_wishlist

    
urlpatterns = [
    path('', views.home, name='home'),  # Added missing quote and name for the path
    path('about/', views.about, name='about'),  # Corrected: 'name/Fabout' to 'name="about"'
    path('contact/', views.contact, name='contact'),  # Corrected: 'name-"contact"' to 'name="contact"'
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),  # Corrected missing quotes
    path('category-title/<val>/', views.CategoryTitle.as_view(), name='category-title'),  # Corrected missing quotes
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),  # Corrected missing quotes
    path('profile/', views.ProfileView.as_view(), name='profile'),  # Corrected missing quotes
    path('address/', views.address, name='address'),  # Corrected missing quotes
    path('updateAddress/<int:pk>/', views.updateAddress.as_view(), name='updateAddress'),  # Corrected missing quotes
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('search/', views.search,name='search'),
    path('wishlist/', views.show_wishlist,name='showwishlist'),
    
    path('pluscart/', views.plus_cart,name='pluscart'),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('plus-wishlist/<int:product_id>/', views.plus_wishlist, name='plus-wishlist'),
    path('minus-wishlist/<int:product_id>/', views.minus_wishlist, name='minus-wishlist'),
    




    # Login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),  # Corrected missing quotes
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),  # Corrected dashes to underscores
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),  # Corrected dashes to underscores
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),  # Corrected dashes to underscores
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Corrected dashes to underscores
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),  # Corrected dashes to underscores
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),  # Corrected dashes to underscores
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),  # Corrected missing quotes
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),  # Corrected missing quotes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin. site. site_header = "Admin Dairy"
admin. site. site_title = "Admin Dairy"
admin. site. site_index_title = "Welcome to Watches Shop"

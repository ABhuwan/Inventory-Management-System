from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),

    path('available/', views.available_products_view, name='available_products'),
    path('add/', views.add_product_view, name='add_product'),
    path('soldout/', views.soldout_view, name='soldout'), 
    path('billing/', views.billing_view, name='billing'),
]
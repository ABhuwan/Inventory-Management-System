<<<<<<< HEAD
from django.http import HttpResponse
from django.shortcuts import render

def aboutus(request):
    return HttpResponse("<h1>heading</h2>")

def home(request):
    return render(request, 'homepage.html')
=======
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, SoldItem

# ---------------- USER AUTH ----------------
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'myapp/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        # User is already logged in → redirect to home
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'myapp/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'myapp/home.html')

# ---------------- PRODUCT MANAGEMENT ----------------
@login_required
def add_product_view(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock")

        if name and price and stock:
            Product.objects.create(
                user=request.user,   # 🔥 IMPORTANT LINE
                name=name,
                price=price,
                stock=stock
            )
            messages.success(request, "Product added successfully!")
            return redirect("add_product")
        else:
            messages.error(request, "All fields are required.")

    # 🔥 Show ONLY this user's products
    products = Product.objects.filter(user=request.user)

    return render(request, "myapp/add.html", {"products": products})

@login_required
def available_products_view(request):
    products = Product.objects.filter(stock__gt=0)
    return render(request, "myapp/available.html", {"products": products})

# ---------------- BILLING ----------------
@login_required
def billing_view(request):
    products = Product.objects.filter(stock__gt=0)

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))

        if quantity <= 0:
            messages.error(request, "Quantity must be at least 1")
            return redirect('billing')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('billing')

        if quantity > product.stock:
            messages.error(request, f"Not enough stock for {product.name}")
            return redirect('billing')

        # Update stock
        product.stock -= quantity
        product.save()

        # Record sale
        total_price = quantity * product.price
        SoldItem.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        messages.success(request, f"Sold {quantity} of {product.name} for ${total_price}")
        return redirect('billing')

    bills = SoldItem.objects.order_by('-sold_at')
    return render(request, 'myapp/billing.html', {'products': products, 'bills': bills})

@login_required
def soldout_view(request):
    sold_items = SoldItem.objects.order_by('-sold_at')
    return render(request, 'myapp/soldout.html', {'sold_items': sold_items})
>>>>>>> 18b1b5ac48db31e36978a9dce696aaf42426a8ea

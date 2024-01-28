from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from .models import Product,Cart,Wishlist,Category,Order

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_products = {}
    for product in products:
        product.actual_price = product.price * 3
    for category in categories:
        category_products[category.name] = Product.objects.filter(category=category)
    return render(request, 'home.html', {'products': products,'category_products': category_products})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

class CollectionView(View):
    template_name = 'collection.html'

    def get(self, request, *args, **kwargs):
        category = kwargs.get('category')
        products = Product.objects.filter(category__name=category)
        context = {'category': category, 'products': products}
        return render(request, self.template_name, context)

class MensCollectionView(CollectionView):
    template_name = 'mens.html'

class WomensCollectionView(CollectionView):
    template_name = 'womens.html'

class AccessoriesCollectionView(CollectionView):
    template_name = 'accessories.html'


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def delete_wishlist_item(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id)

    # Ensure that the user requesting the deletion is the owner of the wishlist item
    if item.user == request.user:
        item.delete()

    return redirect('wishlist')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist') 


@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    user_details = {
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }
    if request.method == 'POST':
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        card_number = request.POST.get('card_number')
        expiration_date = request.POST.get('expiration_date')
        cvv = request.POST.get('cvv')

        # Demo payment details (replace with your logic)
        demo_card_number = '1234567812345678'
        demo_expiration_date = '12/25'
        demo_cvv = '123'

        # Compare with demo details
        if (
            card_number == demo_card_number and
            expiration_date == demo_expiration_date and
            cvv == demo_cvv
        ):
            # Payment successful, proceed with order creation logic
            # Create an order record, handle payment, etc.
            cart_items = Cart.objects.filter(user=request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            order = Order.objects.create(user=request.user, total_price=total_price,address=address,
                pincode=pincode)
            order.products.set([item.product for item in cart_items])
            # Clear the cart
            cart_items.delete()

            messages.success(request, 'Payment successful. Order created!')

            return redirect('home')
        else:
            messages.error(request, 'Payment details are incorrect. Please try again.')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price,'user_details': user_details})

@login_required
def create_order(request):
    if request.method == 'POST':
        # Create an order and associate products with it
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)
        order.products.set([item.product for item in cart_items])

        # Clear the cart after creating the order
        cart_items.delete()

        return render(request, 'order_confirmation.html', {'order': order})

    return redirect('checkout_page')

def sell_with_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')

        if name and description and price and image and category_id:
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                seller=request.user,
                category_id=category_id
            )
            return redirect('product_detail', product_id=product.id)
    else:
        categories = Category.objects.all()
        form_data = {
            'name': '',
            'description': '',
            'price': '',
            'image': None,
            'categories': categories,
        }

    return render(request, 'sell_with_us.html', {'form_data': form_data})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email=request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            # Create a new user
            user = User.objects.create_user(first_name=first_name,
                last_name=last_name,username=username, email=email,password=password)
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('home')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'register.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

@login_required
def user_profile(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email

    context = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'user_orders': user_orders
    }

    return render(request, 'userprofile.html',context)
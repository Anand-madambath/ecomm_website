from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,get_object_or_404
from .forms import CustomUserCreationForm,ProductForm,ReviewForm
from .models import Product,Category,Review
from math import floor
from django.db.models import Avg,Count, Sum
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from .cart import Cart


def home(request):
    products = Product.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    sort = request.GET.get('sort')
    if category:
        products = products.filter(category__id=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if min_rating:
        products = products.filter(avg_rating__gte=min_rating)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-id')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'accounts/customer.html', {
        'page_obj': page_obj,
        'categories': categories,
        'request': request  
    })



def login_redirect_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_product_list')
        elif request.user.role == 'customer':
            return redirect('home')
        else:
            return redirect('login')
    return redirect('home')



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def admin_product_list(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('home')
    products = Product.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    sort = request.GET.get('sort')
    if category:
        products = products.filter(category__id=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if min_rating:
        try:
            products = products.filter(avg_rating__gte=float(min_rating))
        except ValueError:
            pass  
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-id')
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'accounts/admin_product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'request': request  
    })


@login_required
def admin_product_edit(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.method=='POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'accounts/admin_product_edit.html', {'form': form, 'product': product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to delete products.")
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully.')
        return redirect('admin_product_list')
    return redirect('admin_product_list')


@login_required
def add_product(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return HttpResponseForbidden("You are not authorized to add products.")
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'accounts/admin_product_add.html', {'form': form})
    

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    avg_rating = round(avg_rating, 1)
    full_stars = range(int(avg_rating))
    half_star = 1 if avg_rating - int(avg_rating) >= 0.5 else 0
    empty_stars = range(5 - int(avg_rating) - half_star)
    total_reviews = reviews.count()
    total_rating_sum = reviews.aggregate(total=Sum('rating'))['total'] or 0
    form = None
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        if request.method == 'POST' and not user_review:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user  
                review.product = product
                review.save()
                return redirect('product_details', product_id=product.id)
        elif not user_review:
            form = ReviewForm()
    elif request.method == 'POST':
        messages.warning(request, "Please log in to submit a review.")
        return redirect(f"{reverse('login')}?next={request.path}")
    return render(request, 'accounts/product_details.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'total_rating_sum': total_rating_sum,
        'full_stars': full_stars,
        'half_star': half_star,
        'empty_stars': empty_stars,
    })



def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('view_cart')


def update_cart(request, product_id):
    cart = Cart(request)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.update_quantity(product_id, quantity)
    return redirect('view_cart')


def view_cart(request):
    cart = Cart(request)
    return render(request, 'accounts/cart.html', {
        'cart_items': cart.get_items(),
        'total': cart.get_total(),
        'count': cart.get_count()
    })

@login_required
def payment(request):
    return render(request,'accounts/payment.html')

@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html', {
        'user': request.user
    })
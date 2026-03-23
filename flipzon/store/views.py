from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category
# Create your views here.

def home(request):
    featured = Product.objects.filter(available=True, featured=True)[:8]
    latest = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
    'featured': featured,
    'latest': latest,
    'categories': categories,
})

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if search_query:
        products = products.filter(
        Q(name__icontains=search_query) | Q(description__icontains=search_query))

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
        })
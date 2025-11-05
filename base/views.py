from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator
# Create your views here.

def home_page(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 16)
    page = request.GET.get('page') if request.GET.get('page') else 1
    products = paginator.get_page(page)
    context = {
        'products':products,
    }

    return render(request, 'index.html', context)

def detail_page(request, pk):
    product = Product.objects.get(id=pk)
    feature_ids = product.productFeatures.values_list('id', flat=True)

    similar_product = Product.objects.filter(productFeatures__in=feature_ids).exclude(id=product.id)[:4]
    context = {
        'product':product,
        'similar_p':similar_product,
    }

    return render(request, 'detail.html', context)
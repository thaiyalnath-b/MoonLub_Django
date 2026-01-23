from django.shortcuts import render

from .models import Product
# Create your views here.
def productsView(request):
    template = 'products/product.html'
    context = {
        'current_page' : 'products',
        'products' : Product.objects.all()
    }

    return render(request, template_name=template, context=context)

# search Products
from django.db.models import Q
def searchProductS(request):
    template = 'products/search_results.html'
    query = request.GET.get('query_text')
    if query:
        search_results = Product.objects.filter(
            Q(title__icontains = query) |
            Q(desc__icontains = query)
        )

        context = {
            'query' : query,
            'products' : search_results
        }
    else:
        context ={
            'query' : query,
            'prducts' : None
        }
    return render(request, template_name=template, context=context)

# CRUD Operations using Generic Class Based Vies of Django
from django.views.generic import (CreateView, DetailView,
                                    UpdateView, DeleteView)

class CreateProduct(CreateView):
    model = Product
    template_name = 'products/add_product.html'
    fields = '__all__'
    success_url = '/'

from django.views.generic.edit import FormMixin
from .forms import ProductImageForm

class ProductDetail(FormMixin, DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'product'
    form_class = ProductImageForm

    def get_queryset(self):
        return Product.objects.prefetch_related('images')
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['ExtraDetail'] = 'This is Extra Added Details'
    #     return context

class UpdateProduct(UpdateView):
    model = Product
    template_name = 'products/update_product.html'
    fields = '__all__'
    success_url = '/'

class DeleteProduct(DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    fields = '__all__'
    success_url = '/'
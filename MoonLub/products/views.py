from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from .models import Product

from .forms import ProductForm, ProductImageForm
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
        return render(request, template_name=template, context=context)
    else:
        return redirect(reverse_lazy('home_page'))

# CRUD Operations using Generic Class Based Vies of Django
from django.views.generic import (CreateView, DetailView,
                                    UpdateView, DeleteView)

class CreateProduct(CreateView):
    model = Product
    template_name = 'products/add_product.html'
    form_class = ProductForm
    success_url = '/'

from django.views.generic.edit import FormMixin

class ProductDetail(FormMixin, DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'product'
    form_class = ProductImageForm

    def get_success_url(self):
        return reverse("product_details", kwargs={'pk':self.object.pk})
    
    def post(self, request, *ars, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            image = form.save(commit = False)
            image.product = self.object
            image.save()
            return redirect(self.get_success_url())

    def get_queryset(self):
        return Product.objects.prefetch_related('images')
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['ExtraDetail'] = 'This is Extra Added Details'
    #     return context

class UpdateProduct(UpdateView):
    model = Product
    template_name = 'products/update_product.html'
    form_class = ProductForm
    success_url = '/'

class DeleteProduct(DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = '/'

# Edit Product Image
from .models import ProductImage

class EditProductImage(UpdateView):
    model = ProductImage
    template_name = 'products/image_edit.html'
    form_class = ProductImageForm
    context_object_name = 'image'

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.product.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context
    
class DeleteProductImage(DeleteView):
    model = ProductImage
    template_name = 'products/image_delete.html'
    context_object_name = 'image'

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.product.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context
    
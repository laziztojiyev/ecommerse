

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from apps.forms import OrderModelForm
from apps.models import Product, Wishlist, ProductImage, Order


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'apps/product grid.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')

        try:
            product_list_p = paginator.page(page)
        except PageNotAnInteger:
            product_list_p = paginator.page(1)
        except EmptyPage:
            product_list_p = paginator.page(paginator.num_pages)
        contex['product_list'] = product_list_p
        return contex


class ProductImageView(TemplateView):
    model = ProductImage
    template_name = 'apps/product_detail.html'
    context_object_name = 'product_image'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product_detail.html'
    context_object_name = 'product'


class WishlistView(View):
    def get(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product_id=kwargs['product_id'])
        if not created:
            wishlist.delete()
        return redirect('product_list')


class OrderView(FormView):
    form_class = OrderModelForm
    template_name = 'apps/product_detail.html'

    def form_valid(self, form):
        obj = form.save()
        return redirect(reverse('ordered', kwargs={'pk': obj.pk}))

    def form_invalid(self, form):
        return redirect(reverse('product_detail', kwargs={'pk': self.request.POST.get('product')}))



class OrderedView(DetailView):
    template_name = 'apps/ordered.html'
    model = Order
    context_object_name = 'order'


class DeleteOrderedView(DeleteView):
    model = Order
    success_url = reverse_lazy('product_detail')
    template_name = 'apps/ordered.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('pk')
        # You can now use the order_id variable to access the current order ID
        context['order_id'] = order_id
        return context







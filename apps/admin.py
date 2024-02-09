from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.models import Category, Product, Wishlist, Cart


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'image_show', 'category']
    form = ProductModelForm
    list_per_page = 10

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ProductAdmin, self).get_queryset(request)

        #     return super(ProductAdmin, self).get_queryset(request)
        else:
            qs = super(ProductAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='100' height='100' />".format(obj.image.url))

        return 'None'

    image_show.__name__ = 'images'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

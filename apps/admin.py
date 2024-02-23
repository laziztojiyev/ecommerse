from django.contrib import admin
from django.contrib.admin import StackedInline
from django.utils.safestring import mark_safe

from apps.forms import ProductModelForm
from apps.models import Category, Product, Wishlist, Cart, ProductImage, SiteSettings


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ProductImagesStackedInline(StackedInline):
    model = ProductImage
    min_num = 1
    extra = 0
    fields = ['image', ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImagesStackedInline,)
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
        if obj.images.first():
            return mark_safe("<img src='{}' width='100' height='100' />".format(obj.images.first().image.url))

        return 'None'

    image_show.__name__ = 'images'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

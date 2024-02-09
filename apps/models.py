from datetime import timedelta

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import CharField, DateTimeField, DecimalField, ForeignKey, CASCADE, ImageField, JSONField, \
    PositiveIntegerField, IntegerField, SlugField
from django.utils.text import slugify
from django.utils.timezone import now
from django_resized import ResizedImageField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# # Create your models here.
class Category(MPTTModel):
    name = CharField(max_length=255, unique=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'{self.name}'

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'kategoriya'
        verbose_name_plural = 'kategoriyalar'


class Wishlist(models.Model):
    user = ForeignKey('users.CustomUser', CASCADE)
    product = ForeignKey('apps.Product', CASCADE, 'wishlists')
    added_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product}'

    class Meta:
        verbose_name = 'sevimli'
        verbose_name_plural = 'sevimlilar'


class Cart(models.Model):
    user = ForeignKey('users.CustomUser', CASCADE)
    product = ForeignKey('apps.Product', CASCADE, 'products')
    quantity = PositiveIntegerField(default=1)
    added_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} ning savatida: {self.product.name} x {self.quantity}'

    class Meta:
        verbose_name = 'savatcha'
        verbose_name_plural = 'savatchalar'


class Product(models.Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    slug = SlugField(max_length=255, null=True, blank=True)
    Description = RichTextField()
    category = ForeignKey('apps.Category', CASCADE)
    shipping_cost = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = IntegerField()
    image = ResizedImageField(size=[500, 300], upload_to='product_images/', null=True, blank=True)
    characteristics = JSONField(default=dict)
    quantity = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'mahsulot'
        verbose_name_plural = 'mahsulotlar'
        ordering = ('-created_at', )

    @property
    def is_available(self):
        return self.quantity > 0

    @property
    def discount_price(self):
        return self.price * self.discount / 100

    @property
    def sell_price(self):
        return self.price - self.discount_price

    @property
    def is_new(self):
        return self.created_at >= now() - timedelta(days=2)


class Order(models.Model):
    name = CharField(max_length=255)
    phone_number = CharField(max_length=20)
    product = ForeignKey('apps.Product', CASCADE)

    class Meta:
        verbose_name = 'buyurtma'
        verbose_name_plural = 'buyurtmalar'

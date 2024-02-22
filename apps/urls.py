from django.urls import path

from apps.views import ProductListView, ProductDetailView, WishlistView, OrderView, OrderedView, DeleteOrderedView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/add/<int:product_id>', WishlistView.as_view(), name='wishlist_create'),
    path('order', OrderView.as_view(), name='order'),
    path('ordered/<int:pk>', OrderedView.as_view(), name='ordered'),
    path('order/<int:pk>/delete', DeleteOrderedView.as_view(), name='delete_ordered')
]

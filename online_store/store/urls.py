from django.urls import path
from store import views

from .views import (
    # StoreListView,
    ProductDetailView,
)


urlpatterns = [
    path('', views.home, name='home'),

    path('store/', views.store, name='store'),
    # path('store/', StoreListView.as_view(), name='store'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('order_history/', views.order_history, name='order_history'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),

    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
]
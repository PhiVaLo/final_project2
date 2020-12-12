from django.core.paginator import Paginator

from django.shortcuts import render
from django.http import JsonResponse

from datetime import datetime
import json

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,

    TemplateView
)

from users.models import Profile
from .models import (
    # Customer,
    Product,
    Category,
    Order,
    OrderItem,
    ShippingAddress,
)
from . utils import cookieCart, cartData, guestOrder

# =====================================================================================

# Create your views here.
def home(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/home.html', context)

# =====================================================================================

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

# =====================================================================================

# class StoreListView(TemplateView):
#     template_name = 'store/store.html'
#     paginate_by = 3


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         return context

# =====================================================================================

def cart(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

# =====================================================================================

def checkout(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

# =====================================================================================

def order_history(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/order_history.html', context)

# =====================================================================================

class ProductDetailView(DetailView):
    model = Product


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     if self.request.user.is_authenticated:
    #         profile = self.request.user.profile
    #         order, created = Order.objects.get_or_create(profile=profile, complete=False)
    #         items = order.orderitem_set.all()
    #         cartItems = order.get_cart_items        
    #     else:
    #         items = []
    #         order = {'get_cart_total': 0, 'get_cart_items': 0}
    #         cartItems = order['get_cart_items']                

    #     context = {'items': items, 'order': order, 'cartItems': cartItems}        


    #     return context

# =====================================================================================

def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    print('Action:', action)
    print('product_id:', product_id)

    profile = request.user.profile
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(profile=profile, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove' and order_item.quantity > 1:
        order_item.quantity = (order_item.quantity - 1)
    elif action =='delete':
        order_item.quantity = 0

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)

# =====================================================================================

def process_order(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        profile = request.user.profile
        order, created = Order.objects.get_or_create(profile=profile, complete=False)
    else:
        # !=!=!=!=!=!=!=!=!=!=!
        # !=!=!=!=!=!=!=!=!=!=!
        # !=!=!=!=!=!=!=!=!=!=!
        # !=!=!=!=!=!=!=!=!=!=!
        # !=!=!=!=!=!=!=!=!=!=!
        profile, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if float(total) == float(order.get_cart_total):  # total is 'str' and get_cart_total is 'decimal'
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        profile=profile,
        order=order,
        address1=data['shipping']['address1'],
        address2=data['shipping']['address2'],
        country=data['shipping']['country'],
        city=data['shipping']['city'],
        zip_code=data['shipping']['zipcode'],
    )    

    return JsonResponse('Payment complete!', safe=False)

# =====================================================================================
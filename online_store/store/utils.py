import json
from . models import *
from users.forms import UserRegisterForm
from users.models import Profile


def cookieCart(request):
    # cookie cart - if for some reason the cookie is deleted, then make an empty cart
    try:
        cart = json.loads(request.COOKIES['cart'])
    except :
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']        

    # update the cart number
    for i in cart:
        # if a product is ordered, but the product gets removed from the database
        # then ignore this step
        try: 
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)  # product id on cart
            total = (product.price * cart[i]['quantity'])  # total of that product

            order['get_cart_total'] += total  # total of entire order
            order['get_cart_items'] += cart[i]['quantity']  # total quantity

            # build out a cart and the actual items in it without having to
            # store the actual information in the database 
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass

    return {'items': items, 'order': order, 'cartItems': cartItems}

# ===============================================================================

def cartData(request):
    # logged in
    if request.user.is_authenticated:
        # getting the customer
        profile = request.user.profile
        # quering the order (or create it if it doesn't exist yet)
        order, created = Order.objects.get_or_create(profile=profile, complete=False)  # Video part-2 - 36:40
        # get all the order items with this 'order' above as parent (query child object)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items        
    else:
        # not logged in
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return {'items': items, 'order': order, 'cartItems': cartItems}

# ===============================================================================

def guestOrder(request, data):
    print('User is not logged in..')

    print('COOKIES:', request.COOKIES)
    first_name = data['form']['first_name']
    last_name = data['form']['last_name']
    email = data['form']['email']

    # get the data from our cookie cart
    cookieData = cookieCart(request)
    items = cookieData['items']

    # create the customer
    #   If a guess user shops a few times without creating an account,
    #   we don't have to create a new user each time that person checks out.
    #   If this customer creates an account with this same email,
    #   we can attach all of his previous order to this account

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Part 4 - 52:100
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    profile, created = Profile.objects.get_or_create(
        email=email,
    )
    profile.first_name = first_name
    profile.last_name = last_name
    profile.save()

    order = Order.objects.create(
        profile=profile,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

    orderItem = OrderItem.objects.create(
        product=product,
        order=order,
        quantity=item['quantity'],
    )

    # return profile, order
    return order
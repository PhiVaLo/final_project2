from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from users.models import Profile


# # Create your models here.
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # if user is deleted - also delete its items
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.name





class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # digital = models.BooleanField(default=False, null=True, blank=False)
    image =  models.ImageField(default='default-product.jpg', upload_to='product_images', null=True, blank=True)
    description = models.CharField(default='No description', max_length=2000, null=True, blank=True)

    category = models.IntegerField(null=True, blank=True)
    featured = models.BooleanField(null=True, blank=True, default=False)
    image_subs1 =  models.ImageField(upload_to='product_images', null=True, blank=True)
    image_subs2 =  models.ImageField(upload_to='product_images', null=True, blank=True)
    image_subs3 =  models.ImageField(upload_to='product_images', null=True, blank=True)
    image_subs4 =  models.ImageField(upload_to='product_images', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        # # override old user image on upload (except for the default image)
        try:
            this = Product.objects.get(id=self.id)
            if this.image != self.image and this.image != 'default-product.jpg':
                this.image.delete(save=False)
        except:
            pass

        super(Product, self).save()

        # try:
        #     # open the image (of the current instance)
        #     img = Image.open(self.image.path)

        #     # specify the image size (scale down)
        #     if img.height > 300 or img.width > 300:
        #         output_size = (300, 300)
        #         img.thumbnail(output_size)
        #         img.save(self.image.path)    
        # except:
        #     pass



class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)  # if customer is deleted - don't delete the order, just set the customer value to null
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)  # if customer is deleted - don't delete the order, just set the customer value to null
    date_order = models.DateTimeField(auto_now=True)  # then we can change the value whenever that order is set to complete
    # date_order = models.DateTimeField(auto_now_add=True)  # then we can change the value whenever that order is set to complete
    # date_order = models.DateTimeField(default=timezone.now)  # then we can change the value whenever that order is set to complete
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)  # can't return an integer for that string value

    # @property
    # def shipping(self):
    #     shipping = False
    #     orderitems = self.orderitem_set.all()        
    #     for i in orderitems:
    #         if i.product.digital == False:
    #             shipping = True
    #     return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()  # query all the child order items
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity  for item in orderitems])
        return total






class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)  # then we can change the value whenever that order is set to complete

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total




class ShippingAddress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)   # if an order for some reason gets deleted, I would still like to have a shipping address for a customer
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=200, null=True)
    address1 = models.CharField(max_length=200, null=True)
    address2 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    # state = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)  # then we can change the value whenever that order is set to complete

    def __str__(self):
        return f'{self.address1}, {self.address2}'
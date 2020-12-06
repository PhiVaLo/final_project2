from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from django.core.validators import RegexValidator
from django_countries.fields import CountryField



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    # email = models.EmailField()

    image = models.ImageField(default='default-profile.jpg', upload_to='profile_images')

    date_of_birth = models.DateField(blank=True, null=True)

    country = CountryField(null=True)
    city = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=12, null=True)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)

    phone_regex = RegexValidator(regex=r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", message=("Enter a valid international mobile phone number starting with +(country code)"))    
    phone = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)

    additional_information = models.CharField(max_length=2000, null=True, blank=True)


    def save(self, *args, **kwargs):
        # override old user image on upload (except for the default image)
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image and this.image != 'default-profile.jpg':
                this.image.delete(save=False)
        except:
            pass

        super(Profile, self).save(*args, **kwargs)

        # open the image (of the current instace)
        img = Image.open(self.image.path)

        # specify the image soze (scale down)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username} Profile'




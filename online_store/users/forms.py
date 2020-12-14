from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# from django.forms import Textarea

from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django_countries.fields import CountryField

# alphanumberic and space
alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')

# unique email
User._meta.get_field('email')._unique = True

# Date Calendar
class DateInput(forms.DateInput):
    input_type = 'date'

# Country Choice Field - add '---' as the first value
from django_countries import countries
COUNTRY_CHOICES = list(countries)
COUNTRY_CHOICES.insert(0, (None, '---'))



class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, validators=[alphanumeric])
    last_name = forms.CharField(max_length=30, validators=[alphanumeric])
    email = forms.EmailField()

    date_of_birth = forms.DateField(widget=DateInput(), required=False)

    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=12)
    address1 = forms.CharField(label="Address", max_length=200)
    # address2 = forms.CharField(max_length=200, required=False)

    phone_regex = RegexValidator(regex=r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", message=("Enter a valid international mobile phone number starting with +(country code)"))
    phone = forms.CharField(validators=[phone_regex], max_length=17, required=False)

    # additional_information = forms.CharField(max_length=2000, widget=forms.Textarea)


    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'first_name', 
            'last_name',

            'date_of_birth',
            'country',
            'city',
            'zip_code',
            'address1',
            # 'address2',
            'phone',
            # 'additional_information',
            ]


    # convert all email to lowercase - now all emails are unique and case insensitive
    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower().capitalize()





class UserUpdateForm(forms.ModelForm):
    # we want to update only the (username and email) first_name
    email = forms.EmailField()
    # first_name = forms.CharField(max_length=30, required=False, validators=[alphanumeric])
    # last_name = forms.CharField(max_length=30, required=False, validators=[alphanumeric])


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower().capitalize()

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        
        while '  ' in data:
            data = data.replace('  ', ' ')
        return data


class ProfileUpdateForm(forms.ModelForm):
    # update the profile fields
    additional_information = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ['image', 'date_of_birth', 'country', 'city', 'zip_code', 'address1', 'address2', 'phone', 'additional_information']
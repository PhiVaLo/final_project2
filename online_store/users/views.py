from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .forms import UserUpdateForm, ProfileUpdateForm

from django.contrib.auth import login, authenticate

# Create your views here.
def register(request):
    # if the method is a POST-request
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Register model form with POST-request data
        # if the form is submitted and valid
        if form.is_valid():
            user = form.save()  # save the new account created
            username = form.cleaned_data.get('username')  # then grab the username that was submitted
            messages.success(request, f'Account created for {username}!')  # flash message

            user.refresh_from_db()
            # user.profile.display_name = form.cleaned_data.get('display_name')
            user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
            user.profile.address1 = form.cleaned_data.get('address1')
            user.profile.address2 = form.cleaned_data.get('address2')
            user.profile.zip_code = form.cleaned_data.get('zip_code')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.additional_information = form.cleaned_data.get('additional_information')
            user.save()
            
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)


            return redirect('home')
    else:
        # otherwise instantiate an empty form
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

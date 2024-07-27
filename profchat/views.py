from django.shortcuts import render, redirect
import requests
from studentsconnect.models import University, UserProfile, Country, University
from django.contrib import messages
from django.contrib.auth.models import User
from studentsconnect.forms import UserForm, UserProfileForm




def home(request):
    return render(request, 'home.html', {})


def profile_list(request):
    if request.user.is_authenticated:
        # Fetch all countries and universities for the filter dropdowns
        countries = Country.objects.all()
        universities = University.objects.all()
        
        # Get the filter parameters from the query
        country_id = request.GET.get('country', None)
        university_id = request.GET.get('university', None)

        # Filter profiles based on the selected country and university
        profiles = UserProfile.objects.exclude(user=request.user)
        if country_id:
            profiles = profiles.filter(country_id=country_id)
        if university_id:
            profiles = profiles.filter(university_id=university_id)
        
        # Pass profiles, countries, and universities to the template
        return render(request, 'profile_list.html', {
            'profiles': profiles,
            'countries': countries,
            'universities': universities,
            'selected_country': country_id,
            'selected_university': university_id
        })
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('studentsconnect:index')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user_id=pk)

        if request.method == "POST":
            current_user_profile = request.user.userprofile
            action = request.POST['follow']

            if action == "unfollow" and current_user_profile in profile.followed_by.all():
                current_user_profile.follows.remove(profile)
            elif action == "follow" and current_user_profile not in profile.followed_by.all():
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, "profile.html", {"profile":profile})
    else:
        messages.success(request, ("You Must be logged in to view this page"))
        return redirect('studentsconnect:index')
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_profile, created = UserProfile.objects.get_or_create(user=current_user)

        if request.method == "POST":
            user_form = UserForm(request.POST, instance=current_user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                password = user_form.cleaned_data['password']
                if password:
                    user.set_password(password)
                else:
                    user.password = current_user.password
                user.save()
                profile_form.save()
                messages.success(request, ("Your profile was successfully updated!"))
                return redirect('profchat:profile', pk=current_user.id)
        else:
            user_form = UserForm(instance=current_user)
            profile_form = UserProfileForm(instance=user_profile)

        return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('studentsconnect:index')


from django import forms
from studentsconnect.models import Country, Page, Category, University
from django.contrib.auth.models import User
from studentsconnect.models import UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(required=False, help_text="Upload a picture for this category.")

    # An inline class to provide additional information on the form.
    class Meta:
    # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name', 'picture')

class PageForm(forms.ModelForm):

    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
    # Provide an association between the ModelForm and a model
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return password
        return None
    
class UserProfileForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="Select your country"
    )

    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=False,
        empty_label="Select your university"
    )

    class Meta:
        model = UserProfile
        fields = ('website', 'picture', 'country', 'profile_bio', 'university')

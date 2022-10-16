from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

GENDER = ( ('Male','MALE') , ('Female','FEMALE') )  

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter College Id', 'id': 'username'}
                                                      ), required=True, max_length=50)
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter First Name', 'id': 'first_name'}
                               ), required=True, max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name', 'id': 'last_name'}
                                                       ), required=True, max_length=50)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Personal Email', 'id': 'email'}
                                                    ), required=True, max_length=50)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'id': 'password1'}
                                   ), required=True, max_length=50)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Confirm Password', 'id': 'password2'}
                                   ), required=True, max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'id': 'phone', 'placeholder': 'Enter Phone Number'}
                                                   ), required=True, max_length=10, min_length=10)
    location = forms.CharField(widget=forms.TextInput(attrs={'id': 'location', 'placeholder': 'Enter Location'}
                                                   ), required=True)                                           
    gender = forms.CharField(widget=forms.Select(choices=GENDER, attrs={'id': 'gender'}), required=True)
    dob = forms.DateField()

    class Meta:
        model = Profile
        fields = ['phone', 'gender','location','dob']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput(attrs={'class': 'xyz'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                widget=forms.TextInput(attrs={'class': 'xyz'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

# class ProfileUpdateForm(forms.ModelForm):
#     phone = forms.CharField(widget=forms.TextInput(attrs={'id': 'phone', 'placeholder': 'Enter Phone Number'}
#                                                    ), required=True, max_length=10, min_length=10)
#     location = forms.CharField(widget=forms.TextInput(attrs={'id': 'location', 'placeholder': 'Enter Location'}
#                                                    ), required=True)                                           
#     gender = forms.CharField(widget=forms.Select(choices=GENDER, attrs={'id': 'gender'}), required=True)
#     dob = forms.DateField()

#     class Meta:
#         model = Profile
#         fields = ['phone', 'gender','location','dob']
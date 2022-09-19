from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm

from django import forms
from django.db import transaction
from .models import DEPT_CHOICES, GENDER_CHOICES, User,Student,Ngo


from django.contrib.auth import get_user_model


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name= forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
    department = forms.ChoiceField(choices  = DEPT_CHOICES,required=True)
    gender = forms.ChoiceField(choices = GENDER_CHOICES,required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        
    def clean_username(self):
        username = self.cleaned_data.get('username')  # get the username data
        uppercase_username = username.upper()         # get the uppercase version of it
        return uppercase_username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')  # get the email data
        lowercase_email = email.lower()         # get the uppercase version of it
        return lowercase_email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.is_active = False
        user.save()
        student = Student.objects.create(user=user)
        student.phone_number=self.cleaned_data.get('phone_number')
        student.department=self.cleaned_data.get('department')
        student.gender=self.cleaned_data.get('gender')
        student.save()

        return user

class NgoSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)
    phone_number = forms.IntegerField(required=True)
    address = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')  # get the username data
        uppercase_username = username.upper()         # get the uoppercase version of it
        return uppercase_username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')  # get the username data
        lowercase_email = email.lower()         # get the uppercase version of it
        return lowercase_email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_ngo = True
        user.is_staff = True
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        ngo = Ngo.objects.create(user=user)
        ngo.phone_number=self.cleaned_data.get('phone_number')
        ngo.address=self.cleaned_data.get('address')
        ngo.save()
        return user


## added fields
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email']

# class SetPasswordForm(SetPasswordForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['new_password1', 'new_password2']

# class PasswordResetForm(PasswordResetForm):
#     def __init__(self, *args, **kwargs):
#         super(PasswordResetForm, self).__init__(*args, **kwargs)




from django import forms
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm ,UserChangeForm
from users.models import User
class UserLoginForm(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'your_login','placeholder':'Введіть ваш Логін'    
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'your_password','placeholder':'Введіть пароль'
    }))
    class Meta:
        model=User
        fields=('username','password')

class UserRegistrationForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':'full_name','placeholder':'Введіть повне ім’я'    
    }))
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'new_login','placeholder':'Введіть Логін'    
    }))
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'class':'new_email','placeholder':'you@example.com'    
    }))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'new_password','placeholder':'Введіть пароль'    
    }))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'confirm_password','placeholder':'Повторіть пароль'    
    }))
      
    
    class Meta:
        model=User
        fields=('first_name','username','email','password1','password2')

class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'full_name'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control','readonly':True
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control','readonly': True
    }))
class Meta:
        model = User
        fields = ['first_name', 'username', 'email']
